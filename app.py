import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

base_dir_path = os.path.dirname(os.path.realpath(__file__))
downloads_dir_path = os.path.join(base_dir_path, 'data/downloads')

def dir_to_list(dir: str):
    dir_list = os.listdir(dir)
    return dir_list


@app.route("/", methods=["GET"])
def index():
    downloads = dir_to_list(downloads_dir_path)
    return render_template("index.html", downloads=downloads)

@app.route("/scrape_form", methods=["POST"])
def scrape_form():
    try:
        url_to_scrape = request.form.get("url", "").strip()
        if not url_to_scrape:
            raise ValueError("No URL provided")
        
        # Placeholder for scraping function scrape(url_to_scrape)
        print("Scraping:", url_to_scrape)
        print("Scraped:", url_to_scrape)
        print("Images saved to downloads folder.")

    except ValueError as e:
        print("Error:", e)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)