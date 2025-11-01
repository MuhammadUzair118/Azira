import unittest
import json
from src.app import app, get_recommendations

class TestRecommendationAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_recommendations_success(self):
        response = self.app.get('/recommend?title=Intro to Python')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('recommendations', data)
        self.assertIsInstance(data['recommendations'], list)
        self.assertGreater(len(data['recommendations']), 0)

    def test_recommendations_missing_title(self):
        response = self.app.get('/recommend')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'A "title" query parameter is required.')

    def test_recommendations_course_not_found(self):
        response = self.app.get('/recommend?title=Non-Existent Course')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 404)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'No recommendations found for "Non-Existent Course". Could not find this course.')

    def test_get_recommendations_logic(self):
        recommendations = get_recommendations('Intro to Python')
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)

        # Check that the original course is not in the recommendations
        self.assertNotIn('Intro to Python', recommendations)

        # Check that a highly similar course is in the recommendations
        self.assertIn('Data Science with Python', recommendations)

if __name__ == '__main__':
    unittest.main()
