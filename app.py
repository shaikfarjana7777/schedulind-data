import time
import atexit
import pytesseract
from PIL import Image
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def extract_data_from_tiff(image_file):
    try:
        image = Image.open(image_file)
        extracted_text = pytesseract.image_to_string(image)
        print(extracted_text)
        print("Data extracted from TIFF image at", time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    except Exception as e:
        print("Error occurred during data extraction:", str(e))

@app.route("/")
def home():
    return redirect("/upload")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]
            extract_data_from_tiff(image_file)
            return redirect("/schedule")  # Redirect to the /schedule route
    return render_template("upload.html")

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        seconds = int(request.form["seconds"])
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=extract_data_from_tiff, args=("/home/farjana/Downloads/tiff2.jpg",), trigger="interval", seconds=seconds)
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
        return "Scheduled job successfully!"
    return render_template("schedule.html")

if __name__ == "__main__":
    app.run(debug=True)



