# Scrapalyzer
This project is a Python course group assignment . AI developer Jensen Yrkeshögskola.


Temporary Readme notes:


-------------------

Flödet:
Webfront där användare matar in en url

Weburl skickas till scraper som plockar ut bildadresser, bilder över ett visst antal pixlar.

Scraper loopar in listan på bidladresser i imageutil > imagedownloader som sparar alla bilder till downloads/

Imageutil > imageprocessor förädlar bilderna, t.ex plockar ut varje objekt, resizar sparar ner dom i processed-mappen.

Analyzer, plockar upp filer från processed/, gör en identifiering, analyzern placerar sedan bilderna i motsvarande folder för vilket djur som identifierats, t.ex cats/ eller dogs/.

Webfront listar resultaten i olika spalter.

-------------------


Ansvarsområden:

Scraper - Nahuel

Analyzer - Robin

Web & Interface - Viktor

Imageutilities - Emil
