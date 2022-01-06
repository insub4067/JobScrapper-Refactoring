from flask import Flask, render_template, request, send_file
from functions import scrap_jobs
from db import db, keywords


app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():

    keyword = request.args.get("word")

    return render_template("home.html", keywords=keywords)


@app.route("/search")
def search():

    word = request.args.get("word")

    if word in db:
        jobs = db[word]
        return render_template("result.html", jobs=jobs)

    jobs = scrap_jobs(word)

    return render_template("result.html", jobs=jobs)


if __name__ == "__main__":
    app.run("0.0.0.0", port="8000", debug=True)
