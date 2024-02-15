import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import PCA
from django.shortcuts import render
from django.template import RequestContext

# Load and preprocess the data
file_paths = [
    'dataset/dataset1.csv',
    'dataset/dataset2.csv',
    'dataset/dataset3.csv',
    'dataset/dataset4.csv'
]

dfs = []
for file_path in file_paths:
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
    dfs.append(df)

data = pd.concat(dfs)

# Text preprocessing function
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = word_tokenize(text.lower())  # Tokenization and lowercase conversion
    words = [word for word in words if word.isalpha() and word not in stop_words]  # Remove non-alphabetic tokens and stopwords
    words = [lemmatizer.lemmatize(word) for word in words]  # Lemmatization
    preprocessed_text = ' '.join(words)
    return preprocessed_text

# Apply preprocessing to each document title
data['preprocessed_title'] = data['title'].apply(preprocess_text)

# Vectorize the preprocessed documents using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['preprocessed_title'])

# Apply PCA for dimensionality reduction
pca = PCA(n_components=0.95)  # Preserve 95% of variance
X_pca = pca.fit_transform(X.toarray())

# Cluster the documents using K-means
k = 3  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X_pca)

# Evaluate the clusters using silhouette score
silhouette_avg = silhouette_score(X_pca, kmeans.labels_)
print(f"Silhouette Score: {silhouette_avg}")

# Function to assign new documents to clusters
def assign_to_cluster(new_document):
    new_document_vector = vectorizer.transform([preprocess_text(new_document)])
    new_document_vector_pca = pca.transform(new_document_vector.toarray())
    cluster = kmeans.predict(new_document_vector_pca)[0]
    return cluster

def cluster_form_view(request):
    if request.method == 'POST':
        new_document = request.POST.get('new_document', '')
        cluster = assign_to_cluster(new_document)
        return render(request, 'cluster_result.html', {'new_document': new_document, 'cluster': cluster})
    else:
        return render(request, 'cluster_form.html')
