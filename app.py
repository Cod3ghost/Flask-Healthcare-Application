# Import necessary libraries from Flask and MongoDB
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

# Initialize the Flask application
app = Flask(__name__)

# Connect to MongoDB running locally or remotely; update the URI if using MongoDB Atlas
client = MongoClient("mongodb://localhost:27017/")
db = client['user_data']  # Access 'user_data' database in MongoDB
users_collection = db['users']  # Access or create 'users' collection in the database

# Define route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    # Check if the request is a POST (form submission)
    if request.method == "POST":
        # Collect data from the form fields
        age = request.form["age"]
        gender = request.form["gender"]
        total_income = request.form["total_income"]

        # Collect data from expense fields; use 0 as default if field is empty
        expenses = {
            "utilities": request.form.get("utilities", 0),
            "entertainment": request.form.get("entertainment", 0),
            "school_fees": request.form.get("school_fees", 0),
            "shopping": request.form.get("shopping", 0),
            "healthcare": request.form.get("healthcare", 0)
        }

        # Insert collected data into the MongoDB 'users' collection
        users_collection.insert_one({
            "age": age,
            "gender": gender,
            "total_income": total_income,
            "expenses": expenses
        })

        # Redirect to the same page (or any other page) after form submission
        return redirect("/")

    # Render the HTML form when the page loads (GET request)
    return render_template("index.html")

# Run the application in debug mode (helpful for development)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

