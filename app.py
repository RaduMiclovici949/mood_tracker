from flask import Flask, request, render_template_string, redirect, url_for
import json
import os 
app= Flask(__name__)
DATA_FILE = "mooduri.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        moods = json.load(f)
else:
    moods = []

@app.route("/", methods=["GET","POST"])
def home():
    global moods
    if request.method == "POST":
        mood = request.form.get("mood")
        if mood:
            moods.append(mood)
            with open(DATA_FILE, "w") as f:
                json.dump(moods, f)
        return redirect(url_for("home"))

    return render_template_string("""
        <h1>Mood Tracker</h1>
        <form method="POST">
            <input type"text" name="mood" placeholder="How are you feeling?">
            <button type="submit"> Add Mood</button>
        </form>
        <ul>
        {% for m in moods%}
            <li>{{ m }}</li>
        {% endfor %}
        </ul>
    """, moods=moods)
if __name__ == "__main__":
    app.run(debug=True)
