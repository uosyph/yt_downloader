from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
from os import getenv
from services.mp3 import download_mp3
from services.mp4 import download_mp4

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    video_url = request.form.get("url")
    format_type = request.form.get("format")

    if format_type == "mp3":
        download_mp3(video_url)
        flash("Audio downloaded successfully")
    elif format_type == "mp4":
        download_mp4(video_url)
        flash("Video downloaded successfully")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
