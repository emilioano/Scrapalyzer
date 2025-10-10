import os
import posixpath
import logging
from modules.scraper.scraper import Scraper
from config import DevConfig, ProdConfig
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from modules.analyzer.analyzer import ImageAnalyzer
from modules.utils.imageutil import imageprocessor
from modules.utils.imageremover import imageremover,RecursiveCleaner,FlatCleaner

# MOVE THIS OUT TO UTILS OR ANALYZER
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

# Ensure directory exists
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

# Get sub folders paths and category names
def get_files_by_category(folder):
    category_list = []
    # Get the folder path and folder name for folder and each subfolder
    for folder_path in os.walk(folder):
        dir_path = folder_path[0]
        files_path = sorted(folder_path[2])
        category_name = os.path.basename(os.path.normpath(dir_path))
        # Get all files in this subfolder
        files = [posixpath.join(category_name, item) for item in files_path]
        category = dict(
            path=dir_path,
            # Get the name from the last part of the path, normalized to work across different OS
            name= category_name,
            # Add the files list so the template doesn't need os.listdir
            files=files
        )
        category_list.append(category)

    # Remove the root folder from list if list is not empty
    if category_list:
        category_list.pop(0)

    return category_list

# Route to index function, loads file names from downloads folder
@app.route('/', methods=['GET'])
def index():
    downloads = dir_to_list(app.config["DOWNLOADS_DIR"])
    categories = get_files_by_category(app.config["ANALYZED_DIR"])
    return render_template('index.html', downloads=downloads, categories=categories)

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
        return redirect(url_for('index'))

    # Run the scraper
    scraper = Scraper(url_to_scrape)
    scraper.run()

    # Reload index after url is sent
    return redirect(url_for('index'))

# Route to clear downloads folder
@app.route('/clear_downloads_button', methods=['POST'])
def clear_downloads_button():
    try:
        #(path, dryrun mode)
        flatcleaner = FlatCleaner('data/downloads/',False)
        imageremover(flatcleaner)
    except Exception as error:
        logger.error(f'Error when clearing files: {error}')

    # Reload index after button is triggered    
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
        # Call analyzer on the processed images
        analyzer = ImageAnalyzer()
        analyzer.analyze_images(
            analysed_dir=app.config["PROCESSED_DIR"],
            keywords=keywords_to_analyze
        )
    except ValueError as e:
        logger.error(f' * Input error: {e}')

    # Reload index after keywords are sent
    return redirect(url_for('index'))

# Route to clear analyzed folder recursively
@app.route('/clear_analyzed_button', methods=['POST'])
def clear_analyzed_button():
    try:
        #(path, dryrun mode)
        recursivecleaner = RecursiveCleaner('data/analyzed/',False)
        imageremover(recursivecleaner)
    except Exception as error:
        logger.error(f'Error when clearing files: {error}')

    # Reload index after button is triggered    
    return redirect(url_for('index'))


# Serve files from downloads directory to website
@app.route("/downloads/<path:filename>")
def downloaded_image(filename):
    return send_from_directory(app.config["DOWNLOADS_DIR"], filename)

# Serve files from analyzed directory to website
@app.route("/data/analyzed/<path:filename>")
def analyzed_image(filename):
    return send_from_directory(app.config["ANALYZED_DIR"], filename)

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

    class App_Run_Config():
        def __init__(self, host, port, debug, use_reloader, threaded):
            self.host = host
            self.port = port
            self.debug = debug
            self.use_reloader = use_reloader
            self.threaded = threaded

    dev_app_run_config = App_Run_Config(host='127.0.0.1' if debug else '0.0.0.0', port=8000, debug=debug, use_reloader=debug, threaded=True)

    # Note that production is not implemented
    app.run(
        host=dev_app_run_config.host,
        port=dev_app_run_config.port,
        debug=dev_app_run_config.debug,
        use_reloader=dev_app_run_config.use_reloader,
        threaded=dev_app_run_config.threaded,
    )