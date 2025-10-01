import os
import logging
from flask import Flask, render_template, request, redirect, url_for

# Configure logging
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Base
base_dir_path = os.path.dirname(os.path.realpath(__file__))
# Storage
downloads_dir_path = os.path.join(base_dir_path, 'data/downloads')
processed_dir_path = os.path.join(base_dir_path, 'data/processed')
# Modules
modules_dir_path = os.path.join(base_dir_path, 'modules')
utils_dir_path = os.path.join(base_dir_path, 'modules/utils')
scraper_dir_path = os.path.join(base_dir_path, 'modules/scraper')
analyzer_dir_path = os.path.join(base_dir_path, 'modules/analyzer')
# Analyzed
analyzed_dir_path = os.path.join(base_dir_path, 'data/analyzed')
dogs_dir_path = os.path.join(base_dir_path, 'data/analyzed/dogs')
cats_dir_path = os.path.join(base_dir_path, 'data/analyzed/cats')

# Ensure downloads directory exists
def ensure_folder(folders: str | list) -> None:
    if type(folders) == str:
        folder = folders
        try:
            os.makedirs(folder, exist_ok=True)
            logger.info(f' * Ensured folder exists: {folder}')
        except OSError as e:
            logger.error(f' * Failed to ensure folder: {folder} {e}')
            raise
    elif type(folders) == list:
        try:
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
                logger.info(f' * Ensured folder exists: {folder}')
        except OSError as e:        
            logger.error(f' * Failed to ensure folders: {folders} {e}')
            raise        

# Simple helper function
def dir_to_list(dir: str) -> list:
    if not os.path.exists(dir):
        return []
    return os.listdir(dir)

# Route to index function, loads file names from downloads folder.
@app.route('/', methods=['GET'])
def index():
    downloads = dir_to_list(downloads_dir_path)
    return render_template('index.html', downloads=downloads)

# Route to post url input by the user, sent to scrape
@app.route('/scrape_form', methods=['POST'])
def scrape_form():
    try:
        url_to_scrape = request.form.get('url', '').strip()
        if not url_to_scrape:
            raise ValueError('No URL provided')

        # Placeholder for scraping function scrape(url_to_scrape)
        logger.info(f' * Scraping: {url_to_scrape}')
        logger.info(f' * Scraped: {url_to_scrape}')
        logger.info(' * Images saved to downloads folder.')

    # Placeholder error handling
    except ValueError as e:
        logger.error(f' * Input error: {e}')

    # Reload index after url is sent.
    return redirect(url_for('index'))


if __name__ == '__main__':
    ensure_folder([downloads_dir_path, dogs_dir_path, cats_dir_path, processed_dir_path, modules_dir_path, utils_dir_path, scraper_dir_path, analyzer_dir_path])
    app.run(debug=True, port=8000)
