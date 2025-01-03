from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

# Function to generate passwords
def generate_password(length=12, include_punctuation=False, include_numbers=False):
    characters = string.ascii_letters
    if include_numbers:
        characters += string.digits
    if include_punctuation:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    password = ""
    length = 12
    include_punctuation = False
    include_numbers = False
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        include_punctuation = 'include_punctuation' in request.form
        include_numbers = 'include_numbers' in request.form
        password = generate_password(length, include_punctuation, include_numbers)
    return render_template("index.html", length=length, 
        include_punctuation=include_punctuation, 
        include_numbers=include_numbers,
        password=password)
