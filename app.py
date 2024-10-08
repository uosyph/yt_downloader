from flask import (
    Flask,
    render_template,
    request,
    send_file,
    after_this_request,
    redirect,
    flash,
)
import os
from dotenv import load_dotenv
from services.mp3 import download_mp3
from services.mp4 import download_mp4

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    video_url = request.form.get("url")
    format_type = request.form.get("format")

    try:
        if format_type is None:
            file_path = download_mp3(video_url)
        elif format_type == "on":
            file_path = download_mp4(video_url)
    except Exception as e:
        print(e)
        flash("Not a valid URL")
        return redirect("/")

    file_location = os.path.join(os.getcwd(), file_path)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_location)
        except Exception as e:
            print(f"Error deleting file: {e}")
        return response

    return send_file(file_location, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)
