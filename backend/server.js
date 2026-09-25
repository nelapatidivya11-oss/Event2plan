const express = require("express");
const cors = require("cors");
const path = require("path");
const { spawn } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());

// Serve frontend
app.use(express.static(path.join(__dirname, "../frontend")));

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "../frontend/index.html"));
});

app.post("/generate", (req, res) => {

    const text = req.body.text;

    if (!text || !text.trim()) {
        return res.status(400).json({
            error: "Please enter an event description."
        });
    }

    const pythonScript = path.join(
        __dirname,
        "../nlp/event_nlp.py"
    );

    const pythonProcess = spawn("python", [
        pythonScript,
        text.trim()
    ]);

    let output = "";
    let errorOutput = "";

    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    pythonProcess.on("close", (code) => {

        if (code !== 0) {
            console.error(errorOutput);

            return res.status(500).json({
                error: "NLP processing failed.",
                details: errorOutput
            });
        }

        try {
            const result = JSON.parse(output);

            if (result.error) {
                return res.status(500).json(result);
            }

            res.json(result);

        } catch (error) {
            console.error("Invalid Python output:", output);

            res.status(500).json({
                error: "Could not understand NLP output.",
                raw: output
            });
        }
    });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Event2Plan running on port ${PORT}`);
});
