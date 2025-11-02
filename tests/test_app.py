import unittest
import json
from src.app import app, get_recommendations

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client for the Flask application."""
        self.app = app.test_client()
        self.app.testing = True

    def test_recommend_endpoint(self):
        """Test the /recommend endpoint with a valid course title."""
        # Test case with a known course title
        payload = {'course_title': 'Introduction to Computer Science'}
        response = self.app.post('/recommend', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check if the response contains recommendations
        data = json.loads(response.data)
        self.assertIn('recommendations', data)

    def test_recommend_endpoint_invalid_course(self):
        """Test the /recommend endpoint with a course title that does not exist."""
        # Test case with a course title that is not in the dataset
        payload = {'course_title': 'Non-Existent Course'}
        response = self.app.post('/recommend', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Check if the response indicates no recommendations were found
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'No recommendations found for the given course title.')

    def test_recommend_endpoint_missing_course_title(self):
        """Test the /recommend endpoint with a missing course_title."""
        # Test case where course_title is not provided in the payload
        payload = {}
        response = self.app.post('/recommend', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Check if the response contains an error message
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'course_title is required')

    def test_get_recommendations_logic(self):
        """Test the core recommendation logic directly."""
        # Test the recommendation function with a known course title
        recommendations = get_recommendations('Python for Beginners')

        # Check that the recommendations are not empty
        self.assertFalse(recommendations.empty)

        # Add more specific assertions if you have expected outcomes
        # For example, you could check if certain courses are in the recommendations
        expected_recommendations = ['Data Science with Python']
        self.assertTrue(any(course in recommendations.tolist() for course in expected_recommendations))

    def test_get_recommendations_logic_no_match(self):
        """Test the recommendation logic with a course title that has no matches."""
        # Test the recommendation function with a title that won't match
        recommendations = get_recommendations('Unrelated Course Title')

        # Check that the recommendations list is empty
        self.assertTrue(len(recommendations) == 0)

if __name__ == '__main__':
    unittest.main()
