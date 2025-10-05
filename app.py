import os
import logging
from config import DevConfig, ProdConfig
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from modules.analyzer.analyzer import ImageAnalyzer
from modules.utils.imageutil import imageprocessor

# FLYTTA UT KODEN NEDAN TILL UTILS ELLER ANALYZER
from huggingface_hub import snapshot_download

model_dir = "modules/analyzer/models/vit-base-patch16-224"
needed_files = ["config.json", "pytorch_model.bin", "preprocessor_config.json"]

if not all(os.path.exists(os.path.join(model_dir, f)) for f in needed_files):
    snapshot_download(
        repo_id="google/vit-base-patch16-224",
        local_dir=model_dir,
    )
# --------------------------------------------------

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Ensure downloads directory exists
def ensure_folder(folders: str | list) -> None:
    if isinstance(folders, str):
        folders = [folders]

    if isinstance(folders, list):
        try:
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
                logger.info(f' * Ensured folder exists: {folder}')
        except OSError as e:
            logger.error(f' * Failed to ensure folder(s): {folders} {e}')
            raise

# Simple helper function
def dir_to_list(dir: str) -> list:
    if not os.path.exists(dir):
        return []
    return os.listdir(dir)

# Route to index function, loads file names from downloads folder
@app.route('/', methods=['GET'])
def index():
    downloads = dir_to_list(app.config["DOWNLOADS_DIR"])
    return render_template('index.html', downloads=downloads)

# Route to post url input by the user, sent to scrape
@app.route('/scrape_form', methods=['POST'])
def scrape_form():
    try:
        url_to_scrape = request.form.get('url', '').strip()
        if not url_to_scrape:
            raise ValueError('No URL provided')
        if not url_to_scrape.startswith(("http://", "https://")):
            raise ValueError("Invalid URL")
        
    # Placeholder error handling
    except ValueError as e:
        logger.error(f' * Input error: {e}')

    # Placeholder for scraping function scrape(url_to_scrape)
    logger.info(f' * Scraping: {url_to_scrape}')
    logger.info(f' * Scraped: {url_to_scrape}')
    logger.info(' * Images saved to downloads folder.')

    # Reload index after url is sent
    return redirect(url_for('index'))

# Route to run the analyze script
@app.route('/run_analyze', methods=['POST'])
def run_analyze():
    try:
        # Get the keywords from the form, split into a list using commas
        keywords_to_analyze = request.form.get('keywords', '', type=str).split(',')
        # List comprehension using a for loop
        keywords_to_analyze = [keyword.strip() for keyword in keywords_to_analyze if keyword.strip()]
        if not keywords_to_analyze:
            raise ValueError('No keywords provided.')
        # Call the image processor
        imageprocessor()
        # Call analyzer
        analyzer = ImageAnalyzer()
        analyzer.analyze_images(
            analysed_dir=app.config["DOWNLOADS_DIR"],
            keywords=keywords_to_analyze
        )
    except ValueError as e:
        logger.error(f' * Input error: {e}')

    # Reload index after keywords are sent
    return redirect(url_for('index'))

# Serve files from directory to website
@app.route("/downloads/<path:filename>")
def downloaded_image(filename):
    return send_from_directory(app.config["DOWNLOADS_DIR"], filename)

if __name__ == '__main__':
    # Set if True if Development or False if Production (Production env not implemented)
    USE_DEV = True
    cfg = DevConfig if USE_DEV else ProdConfig
    app.config.from_object(cfg)

    # Configure logging, based on config
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG if app.config.get("DEBUG") else logging.INFO,
    )

    # For each string item in app.config that ends with _DIR, ensure folder
    ensure_folder([v for k, v in app.config.items()
                  if k.endswith("_DIR") and isinstance(v, str)])

    # Get debug based on config
    debug = bool(app.config.get("DEBUG", USE_DEV))

    # Note that production is not implemented
    app.run(
        host="127.0.0.1" if debug else "0.0.0.0",
        port=8000,
        debug=debug,
        use_reloader=debug,
        threaded=True,
    )