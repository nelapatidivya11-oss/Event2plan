const express = require("express");
const cors = require("cors");
const path = require("path");
const { spawn } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());

app.use(express.static(path.join(__dirname, "../frontend")));

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "../frontend/index.html"));
});

app.post("/generate", (req, res) => {

    const text = req.body.text;

    if (!text || text.trim() === "") {
        return res.status(400).json({
            error: "Please enter an event description."
        });
    }

    const python = spawn("python", [
        path.join(__dirname, "../nlp/event_nlp.py"),
        text
    ]);

    let output = "";
    let errorOutput = "";

    python.stdout.on("data", (data) => {
        output += data.toString();
    });

    python.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    python.on("close", (code) => {

        if (code !== 0) {

            console.log("Python Error:");
            console.log(errorOutput);

            return res.status(500).json({
                error: "NLP processing failed."
            });
        }

        try {

            const result = JSON.parse(output);

            console.log("NLP RESULT:");
            console.log(result);

            res.json(result);

        } catch (error) {

            console.log("Invalid Python Output:");
            console.log(output);

            res.status(500).json({
                error: "Could not read NLP result."
            });
        }
    });
});
const PORT = process.env.PORT || 3000;

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Event2Plan running on port ${PORT}`);
});
    