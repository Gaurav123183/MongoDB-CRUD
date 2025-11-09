from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mysecretkey")


mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("DATABASE_NAME", "gauravdb")

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db["employees"]  # main collection


@app.route("/")
def index():
    employees = list(collection.find())
    return render_template("index.html", employees=employees)


@app.route("/add_employee", methods=["POST"])
def add_employee():
    name = request.form.get("name")
    email = request.form.get("email")
    designation = request.form.get("designation")
    salary = request.form.get("salary")

    if name and email and designation and salary:
        employee = {
            "name": name,
            "email": email,
            "designation": designation,
            "salary": float(salary)
        }
        collection.insert_one(employee)
        flash("Employee added successfully!", "success")
    else:
        flash("Please fill all fields.", "danger")

    return redirect(url_for("index"))


@app.route("/update_employee/<string:id>", methods=["POST"])
def update_employee(id):
    name = request.form.get("name")
    email = request.form.get("email")
    designation = request.form.get("designation")
    salary = request.form.get("salary")

    if name and email and designation and salary:
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": name,
                "email": email,
                "designation": designation,
                "salary": float(salary)
            }}
        )
        flash("Employee updated successfully!", "info")
    else:
        flash("All fields required!", "danger")

    return redirect(url_for("index"))

@app.route("/delete_employee/<string:id>")
def delete_employee(id):
    collection.delete_one({"_id": ObjectId(id)})
    flash("Employee deleted successfully!", "warning")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
