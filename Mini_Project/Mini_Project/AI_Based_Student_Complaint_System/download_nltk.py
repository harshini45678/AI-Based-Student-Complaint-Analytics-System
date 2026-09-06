import nltk

packages = [
    "punkt",
    "punkt_tab",
    "stopwords",
    "wordnet",
    "omw-1.4",
    "vader_lexicon"
]

for package in packages:
    print(f"Downloading {package}...")
    nltk.download(package)