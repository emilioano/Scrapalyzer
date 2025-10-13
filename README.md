## Scrapalyzer

Scrapalyzer is a Python group project where we scrape images, process them, classify them with AI and display the result in a web interface

This project is a group assignment at AI developer Jensen Yrkeshögskola.


-------------------

## Project flow:

Web front where a user provides a URL

Scraper fetches image links (filters by pixels)

Image utilities download and preprocess images

Analyzer classifies processed images ({keyword}) 

Web front lists results in different sections

-------------------



## Roles:

Scraper - Nahuel

Analyzer - Robin

Web & Interface - Viktor

Image utilities - Emil


-------------------

## Workflow

```text
[ Nahuel - Scraper ] 
       |
       v
   (downloaded images in data/downloads/)
       |
       v
[ Emil - Image Utils ]
       |
       v
 (preprocessed images in data/processed/)
       |
       v
[ Robin - Classifier ]
       |
       v
 (classification -> data/analyzed/{keyword})
       |
       v
[ Viktor - Web/Flask ]
       |
       v
 (displays results in web page via templates/)

 {keyword} indicates a dynamically generated folder based on the classification result.

```

-------------------

## Installation & Setup

git clone git@github.com:emilioano/Scrapalyzer.git   /   https://github.com/emilioano/Scrapalyzer.git (SSH / HTTPS)

cd Scrapalyzer

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

-------------------

## Project Structure

```plaintext
Scrapalyzer/
├── app.py
├── config.py
├── modules/
│   ├── analyzer/
│   │   ├── __init__.py
│   │   └── analyzer.py
│   ├── scraper/
│   │   └── scraper.py
│   └── utils/
│       ├── __init__.py
|       ├── imagedownloader.py
|       ├── imageremover.py
│       └── imageutil.py
├── data/
|   ├── downloads/
|   ├── processed/
|   └── analyzed/
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   ├── sections/
│   ├── analyze.html
│   ├── downloads.html
│   ├── results.html
│   └── scrape.html
│
├── base.html
├── index.html
├── venv/
├── .gitignore
├── config.py
├── requirements.txt
├── tests/
|   ├── test_app.py
|   ├── test_imageremover.py
|   └── test_imageutil.py
└── README.md
```
