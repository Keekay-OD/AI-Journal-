import openai
import csv
import os


#first commit

# Set up OpenAI API credentials
openai.api_key = "your_api_key_here"

# Set up the prompt that will be used for generating responses

prompt = (
    "This is a diary-like app. You can record your thoughts and feelings here, and get responses from me. "
    "To add an entry, simply type 'add' followed by your message. To look up an entry, type 'lookup' followed by a keyword. "
    "For example, you can type 'add Today was a great day' or 'lookup great day'. "
)

# Set up the CSV file where entries will be stored
CSV_FILE_NAME = "diary.csv"
CSV_FIELDNAMES = ["id", "timestamp", "entry"]
entries = []

# Load existing entries from the CSV file

if not os.path.exists(CSV_FILE_NAME):
    with open(CSV_FILE_NAME, mode="w", newline='') as csv_file:
        fieldnames = ["name", "age", "gender"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

with open(CSV_FILE_NAME, mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        entries.append(row)

#testing


def add_entry(entry):
    """Adds a new entry to the CSV file"""

    timestamp = "TODO: insert timestamp here"  # TODO: replace this with a timestamp
    id = len(entries) + 1
    new_entry = {"id": id, "timestamp": timestamp, "entry": entry}
    entries.append(new_entry)

    # Write the updated entries list to the CSV file

    with open(CSV_FILE_NAME, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)
    return "Entry added"

def lookup_entry(keyword):
    """Looks up an entry containing the given keyword"""
    results = []
    for entry in entries:
        if keyword.lower() in entry["entry"].lower():
            results.append(entry)
    
    if len(results) == 0:
        return "No matching entries found."
    else:
        response = ""
        for result in results:
            response += f"\n\nEntry {result['id']} ({result['timestamp']}):\n{result['entry']}"
        return response
    
    # Main loop that reads input from the user and generates responses using GPT-3
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    elif user_input.lower().startswith("add"):
        entry = user_input[4:].strip()
        response = add_entry(entry)
    elif user_input.lower().startswith("lookup"):
        keyword = user_input[7:].strip()
        response = lookup_entry(keyword)
    else:
        # Generate a response using GPT-3
        response = openai.Completion.create(
            engine="davinci", prompt=prompt + f"You: {user_input}", max_tokens=1024
        ).choices[0].text.strip()
    print(f"AI: {response}")


    