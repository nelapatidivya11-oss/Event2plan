const express = require("express");
const cors = require("cors");
const path = require("path");
const { spawn } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());

// ===============================
// FRONTEND
// ===============================

const frontendPath = path.join(__dirname, "../frontend");

app.use(express.static(frontendPath));

// Open Create Event page
app.get("/", (req, res) => {
    res.sendFile(path.join(frontendPath, "create.html"));
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

    // Python NLP file location
    const pythonScript = path.join(
        __dirname,
        "../nlp/event_nlp.py"
    );

    console.log("Processing event:");
    console.log(text);

    // Run Python NLP
    const pythonProcess = spawn("python", [
        pythonScript,
        text.trim()
    ]);

    let output = "";
    let errorOutput = "";

    // Python normal output
    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    // Python error output
    pythonProcess.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    // Python finished
    pythonProcess.on("close", (code) => {

        console.log("Python exit code:", code);

        // Python failed
        if (code !== 0) {

            console.error("Python Error:");
            console.error(errorOutput);

            return res.status(500).json({
                error: "NLP processing failed.",
                details: errorOutput || "Unknown Python error."
            });
        }

        // Empty output
        if (!output.trim()) {

            return res.status(500).json({
                error: "NLP returned empty output."
            });
        }

        try {

            // Convert Python JSON → JavaScript object
            const result = JSON.parse(output.trim());

            console.log("NLP Result:");
            console.log(result);

            // Python itself returned an error
            if (result.error) {

                return res.status(500).json(result);
            }

            // Send result to frontend
            return res.json(result);

        } catch (error) {

            console.error("JSON parsing error:");
            console.error(error);

            console.error("Python output:");
            console.error(output);

            return res.status(500).json({
                error: "Could not understand NLP output.",
                raw: output
            });
        }
    });

    // Python process error
    pythonProcess.on("error", (error) => {

        console.error("Failed to start Python:");
        console.error(error);

        return res.status(500).json({
            error: "Could not start Python NLP process.",
            details: error.message
        });
    });
});

// ===============================
// SERVER
// ===============================

const PORT = process.env.PORT || 3000;

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Event2Plan running on port ${PORT}`);
});
