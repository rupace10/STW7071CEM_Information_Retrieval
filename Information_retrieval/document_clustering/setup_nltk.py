import nltk

def download_nltk_data():
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

if __name__ == "__main__":
    download_nltk_data()
