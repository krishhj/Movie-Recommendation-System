# Movie-Recommendation-System
This project is a Python-based movie recommendation system that helps users discover new movies. Pick a movie you already love and it finds other movies with similar content.
## Features
### Content-Based Filtering: Recommends movies by comparing movie plots, genres, keywords, cast, and crew.

### Similarity Score: Uses Cosine Similarity to find the movies that are most alike.

### Interactive: Streamlit web interface to get instant recommendations, with posters from the TMDB API.

### Data-Driven: Built on the TMDB 5000 movies and credits dataset.

## 🔧 How It Works
The recommendation logic is built on the concept of "vector space models". Here’s a simplified breakdown:

### Data Preprocessing: Movie data (genres, keywords, overview, top 5 cast with character names, directors and producers) is cleaned, lowercased, stemmed with NLTK's PorterStemmer, and merged into a single text-based feature string for each movie.

### Feature Extraction: A CountVectorizer (5,000 most frequent terms, English stop words removed) converts the text for each movie into a vector of word counts.

### Similarity Calculation: We then compute the Cosine Similarity between these vectors. Cosine similarity measures the cosine of the angle between two vectors, which tells us how similar they are. A score closer to 1 means the movies are very similar. All scores are computed ahead of time and saved in `similarity.pkl`.

### Recommendation: When you select a movie title, the app looks up its row in the saved similarity matrix and returns the 6 other movies with the highest similarity scores.

## 🛠️ Technology Stack
### Language: Python

### Libraries:

### Pandas for data manipulation and analysis.

### NumPy for numerical operations.

### NLTK for stemming, and Scikit-learn for CountVectorizer and cosine similarity calculation (used in the notebook).

### Streamlit and Requests for the web app and TMDB poster lookups.

