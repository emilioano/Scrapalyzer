from modules.analyzer.analyzer import ImageAnalyzer
from modules.utils.imageutil import imageprocessor


keywords = ['cat','dog','monkey','pig','bus','taxi','can','penguin','camera','phone']

input('Tryck enter för att köra imageprocessor')
imageprocessor()

input('Tryck enter för att starta imageanalyzer')

'''
analyzer = ImageAnalyzer()
results = analyzer.analyze_images(
    analysed_dir="data/processed",
    cats_dir="data/analyzed/cats",
    dogs_dir="data/analyzed/dogs"
)
for result in results:
    print(result)
'''
analyzer = ImageAnalyzer()
results = analyzer.analyze_images(
    analysed_dir="data/processed/",
    keywords=keywords
)
for result in results:
    print(result)