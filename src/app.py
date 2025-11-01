from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Construct the absolute path to the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'data', 'courses.csv')

# Load and preprocess the data
df = pd.read_csv(csv_path)
df['combined_features'] = df['course_title'] + ' ' + df['category'] + ' ' + df['skills']

# Initialize and fit the TF-IDF Vectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        idx = df[df['course_title'] == title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        course_indices = [i[0] for i in sim_scores]
        return df['course_title'].iloc[course_indices].tolist()
    except IndexError:
        return []

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'A "title" query parameter is required.'}), 400

    recommendations = get_recommendations(title)

    if not recommendations:
        return jsonify({'message': f'No recommendations found for "{title}". Could not find this course.'}), 404

    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
