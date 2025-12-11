const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const axios = require("axios");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000; // Use environment variable for PORT if available

const FILE_PATH = path.join(__dirname, "survey_responses.json");

// Configure CORS to allow requests from your frontend domain
app.use(
  cors({
    origin: process.env.FRONTEND_URL || "https://www.riho-gen-ai.cs.csusm.edu", // Use environment variable for flexibility
    credentials: true,
  })
);

app.use(express.json()); // Middleware to parse JSON body
console.log("Health Check");
// Health check route
app.get("/", (req, res) => {
  res.status(200).send("Backend server is running. Available routes: /chatgpt, /save-survey");
});
console.log("OpenAI API");
// POST route to call OpenAI API securely
app.post("/chatgpt", async (req, res) => {
  const { question, studentInput, examples } = req.body;
console.log("Validate input data");
  // Validate input data
  if (!question || !studentInput) {
    return res.status(400).json({ message: "Question and studentInput are required." });
  }
console.log("Build Prompt OpenAI API");
  // Build the prompt for OpenAI
  const examplesText = examples ? `Examples: {${examples.join(", ")}}\n` : "";
  const prompt = `Question: ${question}\nReplace the {} with, and the students are allowed to choose any of the examples provided. ${examplesText}\nStudent Answer: ${studentInput}\n\nCompare the student's answer with the correct answer and give suggestions on how to improve the answer.`;
console.log("OpenAI API Response");
  try {
    const response = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4",
        messages: [{ role: "user", content: prompt }],
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.OPENAI_API_KEY}`, // Use environment variable for security
        },
      }
    );
    console.log("Message Content:", response.data.choices[0].message);
    res.status(200).json({ response: response.data.choices[0].message.content });
  } catch (error) {
    console.error("Error calling OpenAI API:", error.response ? error.response.data : error.message);
    res.status(500).json({
      message: "Failed to get response from OpenAI.",
      error: error.response ? error.response.data : error.message,
    });
  }
});

// POST route to save survey data
app.post("/save-survey", (req, res) => {
  const newResponse = req.body;

  // Validate input data
  if (!newResponse || typeof newResponse !== "object") {
    return res.status(400).json({ message: "Invalid survey data." });
  }

  let existingResponses = [];
  if (fs.existsSync(FILE_PATH)) {
    try {
      existingResponses = JSON.parse(fs.readFileSync(FILE_PATH, "utf8"));
    } catch (error) {
      console.error("Error parsing existing JSON file:", error.message);
      return res.status(500).json({ message: "Failed to parse existing data.", error: error.message });
    }
  }

  existingResponses.push(newResponse);

  try {
    fs.writeFileSync(FILE_PATH, JSON.stringify(existingResponses, null, 2));
    console.log("Data saved successfully:", newResponse);
    res.status(200).json({ message: "Data saved successfully!" });
  } catch (error) {
    console.error("Error saving data:", error.message);
    res.status(500).json({ message: "Failed to save data.", error: error.message });
  }
});

// Start the server, listening on all network interfaces
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on http://0.0.0.0:${PORT}`);
});
