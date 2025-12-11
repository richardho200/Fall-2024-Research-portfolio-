from customtkinter import *
from PIL import Image
import pandas as pd
import random
import json
from tkinter import messagebox

# Set the appearance mode to light
set_appearance_mode("light")

# Create an instance of the CTk class
app = CTk()

# Set the size of the window
app.geometry("700x450")

# Set the window title
app.title("CSUSM Data Entry")

# Load student data from CSV file
data_file = r"Student ID DATA BASE(Sheet1).csv"
student_data = pd.read_csv(data_file)

# File paths for JSON data
cs211_json_path = r"CS211.json"
cs311_json_path = r"CS311.json"

# Variables to track the current question and chosen examples
current_question_index = 0
chosen_examples = {}

# Function to create the main page content
def create_main_page():
    global main_frame, name_entry, id_entry, check_211, check_311

    main_frame = CTkFrame(app)
    main_frame.pack(fill="both", expand=True, padx=(20, 20), pady=20)

    # Load the image
    logo_image_path = "Official_CSUSM_Logo.png"
    logo_image = Image.open(logo_image_path)

    # No transparency processing; directly resize the image
    logo_image = logo_image.resize((200, 80), Image.LANCZOS)

    # Convert to a CustomTkinter-compatible CTkImage
    logo_photo = CTkImage(dark_image=logo_image, size=(200, 80))

    # Add the logo image to the main frame
    logo_label = CTkLabel(main_frame, image=logo_photo, text="")
    logo_label.pack(pady=20, padx=20)

    # Add a student name entry field
    name_label = CTkLabel(main_frame, text="Student name:")
    name_label.pack(side="top", pady=(10, 5))
    name_entry = CTkEntry(main_frame)
    name_entry.pack(side="top", pady=(0, 10))

    # Add a student ID entry field
    id_label = CTkLabel(main_frame, text="Student ID:")
    id_label.pack(side="top", pady=(10, 5))
    id_entry = CTkEntry(main_frame)
    id_entry.pack(side="top", pady=(0, 10))
    
    # Create a frame for the checkboxes
    checkbox_frame = CTkFrame(main_frame)
    checkbox_frame.pack(side="top", pady=(10, 5))

    # Add checkboxes for 211 and 311 (you can choose only one)
    check_211 = CTkCheckBox(checkbox_frame, text="For 211")
    check_211.pack(side="left", padx=5)
    check_311 = CTkCheckBox(checkbox_frame, text="For 311")
    check_311.pack(side="left", padx=5)

    # Add button to start the data entry and switch to the next page
    start_button = CTkButton(main_frame, text="Start Data Entry", command=validate_and_proceed)
    start_button.pack(side="top", pady=(20, 0))

# Function to validate the student ID and course selection, then proceed to the next page 
def validate_and_proceed():
    student_id = id_entry.get()
    if not student_id:
        messagebox.showerror("Error", "Please enter a Student ID.")
        return

    if student_id not in student_data['studentID'].astype(str).values:
        messagebox.showerror("Error", "Student ID not available.")
        return
    
    # Determine which checkbox is selected
    cs211_selected = check_211.get()
    cs311_selected = check_311.get()
    
    if cs211_selected and not cs311_selected:
        load_questions(cs211_json_path)
        go_to_next_page()
    elif cs311_selected and not cs211_selected:
        load_questions(cs311_json_path)
        go_to_next_page()
    else:
        messagebox.showerror("Error", "Please choose one CS course.")

# Function to load questions from a JSON file
def load_questions(file_path):
    global questions_data
    with open(file_path, 'r') as file:
        questions_data = json.load(file)['questions']

# Function to switch to the next page
def go_to_next_page():
    global next_page_frame, left_text_display, left_text_input, right_text_display

    # Destroy the main frame
    main_frame.pack_forget()
    main_frame.destroy()

    # Create the next page frame
    next_page_frame = CTkFrame(app)
    next_page_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Create left and right frames inside next_page_frame
    left_frame = CTkFrame(next_page_frame)
    left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
    right_frame = CTkFrame(next_page_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
    
    # Configure left frame for grid layout with equal row heights
    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_rowconfigure(1, weight=1)

    # Add text display box to left frame (top half) with read-only and word wrap
    left_text_display = CTkTextbox(left_frame, wrap="word")
    left_text_display.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
    left_text_display.configure(state="disabled")  # Make the text box read-only
    
    # Add text input box to left frame (bottom half) for multiline input
    left_text_input = CTkTextbox(left_frame, wrap="word")
    left_text_input.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
    
    # Add navigation buttons
    prev_button = CTkButton(left_frame, text="< Prev", command=prev_question)
    prev_button.grid(row=2, column=0, sticky="w", padx=10, pady=10)
    next_button = CTkButton(left_frame, text="Next >", command=next_question)
    next_button.grid(row=2, column=0, sticky="e", padx=10, pady=10)
    
    # Configure right frame for grid layout with equal row heights
    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_rowconfigure(1, weight=1)
    
    # Add text display box to right frame (top half) with read-only and word wrap
    right_text_display = CTkTextbox(right_frame, wrap="word")
    right_text_display.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
    right_text_display.configure(state="disabled")  # Make the text box read-only
    
    # Add rating buttons to right frame (bottom half)
    rating_frame = CTkFrame(right_frame)
    rating_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
    
    # Define button style for circular appearance
    button_style = {
        "width": 10,  # Set width of the button
        "height": 5,  # Set height of the button
        "corner_radius": 20,  # Half of width/height to make the button circular
        "border_width": 1  # Optional: Add border to the button
    }

    one_star_button = CTkButton(rating_frame, text="1 ★", **button_style, command=lambda: rate_answer(1))
    one_star_button.grid(row=0, column=0, padx=(1, 2), pady=3)

    two_star_button = CTkButton(rating_frame, text="2 ★", **button_style, command=lambda: rate_answer(2))
    two_star_button.grid(row=0, column=1, padx=(1, 2), pady=3)

    three_star_button = CTkButton(rating_frame, text="3 ★", **button_style, command=lambda: rate_answer(3))
    three_star_button.grid(row=0, column=2, padx=(1, 2), pady=3)

    four_star_button = CTkButton(rating_frame, text="4 ★", **button_style, command=lambda: rate_answer(4))
    four_star_button.grid(row=0, column=3, padx=(1, 2), pady=3)

    five_star_button = CTkButton(rating_frame, text="5 ★", **button_style, command=lambda: rate_answer(5))
    five_star_button.grid(row=0, column=4, padx=(1, 2), pady=3)

    # Center the buttons within the frame
    for i in range(5):
        rating_frame.grid_columnconfigure(i, weight=1)

    # Display the first question
    display_question(current_question_index)

# Function to display a question based on the current index
def display_question(index):
    question_data = questions_data[index]
    question_text = question_data["question"]

    # Replace placeholders with chosen examples or select new ones
    if index in chosen_examples:
        examples = chosen_examples[index]
    else:
        examples = [random.choice(question_data.get("examples", [""])) for _ in question_text.split("{}")[:-1]]
        chosen_examples[index] = examples

    question_text = question_text.format(*examples)
    left_text_display.configure(state="normal")  # Enable writing in the text box
    left_text_display.delete("1.0", "end")
    left_text_display.insert("1.0", question_text)
    left_text_display.configure(state="disabled")  # Make the text box read-only again

# Function to go to the next question
def next_question():
    global current_question_index
    if current_question_index < len(questions_data) - 1:
        current_question_index += 1
        display_question(current_question_index)

# Function to go to the previous question
def prev_question():
    global current_question_index
    if current_question_index > 0:
        current_question_index -= 1
        display_question(current_question_index)

# Function to rate a chatGPT answer
def rate_answer(rating):
    print(f"Answer {current_question_index + 1} rated {rating} stars.")

# Initialize the main page
create_main_page()

# Start the main event loop
app.mainloop()
