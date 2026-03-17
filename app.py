from flask import Flask, request, jsonify, render_template

from auth import get_user, get_user_groups
from agent import run_agent

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user = get_user()

    if not user:
        return jsonify({"response": "Authentication required."})

    groups = get_user_groups()

    question = request.json["message"]

    answer = run_agent(question, user, groups)

    return jsonify({"response": answer})

@app.route("/debug")
def debug():

    groups = get_user_groups()

    return {
        "groups": groups
    }

if __name__ == "__main__":
    app.run()