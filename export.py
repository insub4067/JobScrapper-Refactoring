import csv
from db import db


def export(word):
    print(db.keys())
    file = open("jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "link", "company", "location", "pay"])
    jobs = db.get(word)
    for job in jobs:
        writer.writerow(job.values())
