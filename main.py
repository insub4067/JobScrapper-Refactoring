from flask import Flask, render_template, request, send_file
from scrapper import scrap_jobs
from db import db, keywords
from export import export


app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():

    return render_template("home.html", keywords=keywords)


@app.route("/search")
def search():

    word = request.args.get("word")
    word = word.lower()

    if db.get(word):
        jobs = db[word]
        return render_template("result.html", jobs=jobs, word=word)

    jobs = scrap_jobs(word)

    return render_template("result.html", jobs=jobs, word=word)


@app.route("/export")
def file():
    word = request.args.get("word")
    word = word.lower()
    if not word:
        raise Exception()
    jobs = db[word]
    if not jobs:
        raise Exception()
    export(word)
    return send_file("jobs.csv")


if __name__ == "__main__":
    app.run(host="localhost", port="8001", debug=True)
