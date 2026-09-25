const express = require("express");
const cors = require("cors");
const path = require("path");
const { spawn } = require("child_process");

const app = express();

// ===============================
// BASIC SETUP
// ===============================

app.use(cors());
app.use(express.json());

// ===============================
// FRONTEND
// ===============================

const frontendPath = path.join(__dirname, "../frontend");

app.use(express.static(frontendPath));

// Home page
app.get("/", (req, res) => {
    res.sendFile(path.join(frontendPath, "create.html"));
});

// ===============================
// HEALTH CHECK
// ===============================

app.get("/health", (req, res) => {
    res.json({
        status: "OK",
        message: "Event2Plan backend is running"
    });
});

// ===============================
// NLP GENERATION
// ===============================

app.post("/generate", (req, res) => {

    const text = req.body.text;

    // Check input
    if (!text || typeof text !== "string" || !text.trim()) {
        return res.status(400).json({
            error: "Please enter an event description."
        });
    }

    // Python file path
    const pythonScript = path.join(
        __dirname,
        "../nlp/event_nlp.py"
    );

    console.log("--------------------------------");
    console.log("Event2Plan NLP Request");
    console.log("Input:", text);
    console.log("Python Script:", pythonScript);
    console.log("--------------------------------");

    // =================================
    // WINDOWS → python
    // RENDER/LINUX → python3
    // =================================

    const pythonCommand =
        process.platform === "win32"
            ? "python"
            : "python3";

    console.log("Python command:", pythonCommand);

    // Run Python NLP
    const pythonProcess = spawn(
        pythonCommand,
        [
            pythonScript,
            text.trim()
        ],
        {
            cwd: path.dirname(pythonScript)
        }
    );

    let output = "";
    let errorOutput = "";

    // ===============================
    // PYTHON OUTPUT
    // ===============================

    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    // ===============================
    // PYTHON ERROR
    // ===============================

    pythonProcess.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    // ===============================
    // PYTHON PROCESS ERROR
    // ===============================

    pythonProcess.on("error", (error) => {

        console.error("Python process could not start:");
        console.error(error);

        if (!res.headersSent) {
            return res.status(500).json({
                error: "Could not start Python NLP process.",
                details: error.message
            });
        }
    });

    // ===============================
    // PYTHON FINISHED
    // ===============================

    pythonProcess.on("close", (code) => {

        console.log("Python exit code:", code);

        // Python failed
        if (code !== 0) {

            console.error("Python Error:");
            console.error(errorOutput);

            if (!res.headersSent) {
                return res.status(500).json({
                    error: "NLP processing failed.",
                    details:
                        errorOutput ||
                        "Python returned an error."
                });
            }

            return;
        }

        // No output from Python
        if (!output.trim()) {

            console.error("Python returned empty output.");

            if (!res.headersSent) {
                return res.status(500).json({
                    error: "NLP returned empty output."
                });
            }

            return;
        }

        // ===============================
        // CONVERT PYTHON JSON
        // ===============================

        try {

            const result = JSON.parse(output.trim());

            console.log("NLP Result:");
            console.log(result);

            // Python returned an error
            if (result.error) {

                if (!res.headersSent) {
                    return res.status(500).json(result);
                }

                return;
            }

            // Send NLP result to frontend
            if (!res.headersSent) {
                return res.status(200).json(result);
            }

        } catch (error) {

            console.error("JSON parsing error:");
            console.error(error);

            console.error("Raw Python output:");
            console.error(output);

            if (!res.headersSent) {
                return res.status(500).json({
                    error: "Could not understand NLP output.",
                    raw: output
                });
            }
        }
    });
});

// ===============================
// SERVER
// ===============================

const PORT = process.env.PORT || 3000;

app.listen(PORT, "0.0.0.0", () => {

    console.log("--------------------------------");
    console.log("Event2Plan server started");
    console.log(`Running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || "development"}`);
    console.log("--------------------------------");
});
