from modules.analyzer.analyzer import ImageAnalyzer
from modules.utils.imageutil import imageprocessor

input('Tryck enter för att köra imageprocessor')
imageprocessor()

input('Tryck enter för att starta imageanalyzer')
analyzer = ImageAnalyzer()
results = analyzer.analyze_images(
    analysed_dir="data/processed",
    cats_dir="data/analyzed/cats",
    dogs_dir="data/analyzed/dogs"
)
for result in results:
    print(result)