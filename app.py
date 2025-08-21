from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import json
import os
from report import generate_moods_report

app = Flask(__name__)

DATA_FILE = "moods.json"

moods = []


def load_moods():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_moods():
    with open(DATA_FILE, "w") as f:
        json.dump(moods, f)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        mood = request.form.get("mood")
        if mood:
            return redirect(url_for("add_mood", mood_name=mood))
        return redirect(url_for("home"))

    return render_template("home.html", moods=moods)


@app.route("/mood/<mood_name>")
def add_mood(mood_name):
    if mood_name:
        moods.append(mood_name)
        save_moods()

    return render_template("home.html", moods=moods)


@app.route("/report")
def report():
    distribution, path = generate_moods_report()
    return jsonify(distribution)


@app.route("/report/download")
def download_report():
    distribution, path = generate_moods_report(data_file=DATA_FILE)
    return send_file(
        path,
        mimetype="application/json",
        as_attachment=True,
        download_name=os.path.basename(path),
    )


def main():
    global moods
    moods = load_moods()
    app.run(debug=True)


if __name__ == "__main__":
    main()
