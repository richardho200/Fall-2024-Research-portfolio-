const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const axios = require("axios");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;
const HOST = "172.25.96.170";
app.listen(PORT, "0.0.0.0");
const FILE_PATH = path.join(__dirname, "survey_responses.json");

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Backend running");
});

app.post("/chatgpt", async (req, res) => {
  const { question, studentInput, examples } = req.body;

  if (!question || !studentInput) {
    return res.status(400).json({ error: "Missing input" });
  }

  const examplesText = examples?.length
    ? `Allowed examples: ${examples.join(", ")}`
    : "";

  const prompt = `
Question:
${question}

${examplesText}

Student Answer:
${studentInput}

Task:
Give constructive feedback and suggestions for improvement.
`;

  try {
    const response = await axios.post(
      "https://api.openai.com/v1/responses",
      {
        model: "gpt-4.1-mini",
        input: prompt
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );

    res.json({
      response: response.data.output[0].content[0].text
    });

  } catch (err) {
    console.error(err.response?.data || err.message);
    res.status(500).json({ error: "OpenAI call failed" });
  }
});

app.listen(PORT, HOST, () => {
  console.log(`Server running at http://${HOST}:${PORT}`);
});
