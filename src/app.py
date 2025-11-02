from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationEngine:
    def __init__(self, data_path='data/courses.csv'):
        self.df = self._load_data(data_path)
        self._preprocess_data()
        self.cosine_sim = self._calculate_similarity()

    def _load_data(self, data_path):
        try:
            return pd.read_csv(data_path)
        except FileNotFoundError:
            data = {
                'course_id': ['CS101', 'PY201', 'DS301', 'WD401', 'ML501'],
                'course_title': ['Introduction to Computer Science', 'Python for Beginners', 'Data Science with Python', 'Web Development Fundamentals', 'Machine Learning Essentials'],
                'course_description': ['A foundational course on computer science principles.', 'An introductory course to Python programming.', 'A comprehensive guide to data science using Python.', 'Learn the basics of web development, including HTML, CSS, and JavaScript.', 'An essential course on machine learning concepts and algorithms.'],
                'category': ['Computer Science', 'Programming', 'Data Science', 'Web Development', 'Machine Learning'],
                'skills': ['Algorithms, Data Structures', 'Python, Programming', 'Pandas, NumPy, Scikit-learn', 'HTML, CSS, JavaScript', 'Supervised Learning, Unsupervised Learning']
            }
            return pd.DataFrame(data)

    def _preprocess_data(self):
        self.df['course_content'] = self.df['course_title'] + ' ' + self.df['course_description'] + ' ' + self.df['category'] + ' ' + self.df['skills']

    def _calculate_similarity(self):
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.df['course_content'])
        return cosine_similarity(tfidf_matrix, tfidf_matrix)

    def get_recommendations(self, course_title):
        try:
            idx = self.df[self.df['course_title'] == course_title].index[0]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]
            course_indices = [i[0] for i in sim_scores]
            return self.df['course_title'].iloc[course_indices]
        except IndexError:
            return pd.Series([])

app = Flask(__name__)
engine = RecommendationEngine()

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    course_title = data.get('course_title')

    if not course_title:
        return jsonify({'error': 'course_title is required'}), 400

    recommendations = engine.get_recommendations(course_title)

    if not recommendations.empty:
        return jsonify({'recommendations': recommendations.tolist()})
    else:
        return jsonify({'message': 'No recommendations found for the given course title.'}), 404

# This function is needed for the unit tests to access the recommendation logic
def get_recommendations(course_title):
    return engine.get_recommendations(course_title)

if __name__ == '__main__':
    app.run(debug=True)
