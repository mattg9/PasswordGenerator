from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

# Function to generate passwords
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    password = ""
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        password = generate_password(length)
    return render_template("index.html", password=password)
