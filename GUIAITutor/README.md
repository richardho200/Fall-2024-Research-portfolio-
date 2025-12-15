# CSUSM Data Entry Application

This application is designed for entering and managing student data for CSUSM courses. It includes a user-friendly GUI built with `CustomTkinter` and supports multiple functionalities such as student data entry, course selection, and navigation between questionnaire pages.

## Screenshots

### Main Page
![image](https://github.com/user-attachments/assets/44040abb-22a0-4fd4-96ff-05ba2a46efd9)

### Error Message for Multiple Selection
![image](https://github.com/user-attachments/assets/cedee378-870e-411a-8235-15574d985660)


### Question Navigation
![image](https://github.com/user-attachments/assets/7e1b59d1-5b2d-4c8c-851c-425cd215127a)



## Features

- **Student Information Input**: Enter student name and ID.
- **Course Selection**: Choose between CS211 and CS311 courses.
- **Dynamic Content Loading**: Load different question sets based on the selected course.
- **Question Navigation**: Navigate through questions with a `Prev` and `Next` button.
- **Light Mode**: The application runs in light mode for better visibility.

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AimanMadan/CSUSMDataEntryGUI.git
   cd CSUSMDataEntryGUI
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Requirements

- `CustomTkinter`
- `Pillow`
- `pandas`
- `random`
- `json`

## Script Changes Overview

### Major Changes
1. **Light Mode**: The application now uses a light appearance mode for better readability.
2. **Student Data Loading**: Reads student data from a CSV file for validation.
3. **Dynamic JSON Loading**: Loads questions from different JSON files (`CS211.json` and `CS311.json`) based on the course selected.
4. **Validation Enhancements**: Added validation for course selection and student ID entry.
5. **Navigation and Display**: Implemented navigation between questions with consistent example selection.

###  IMPORTANT: ADDITIONAL Directions for running the program

1)create .env folder and create the API key before you use

create txt file
in the txt file you must have
OPENAI_API_KEY="your-api-key"
PORT=5000

2) Running Node command PRIOR to running the main.py
Server.js is the backend for the API communication to the front end GUI app.
Run these commands for first time ONLY
npm install express cors axios dotenv
node server.js

before running the main.py

After installing the express cors axios dotenv, then you must run node server.js prior running the main.py
