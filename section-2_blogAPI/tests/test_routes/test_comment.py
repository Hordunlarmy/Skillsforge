import unittest
import requests


class TestCOMMENT(unittest.TestCase):
    BASE_URL = "http://localhost:8000"

    def setUp(self):
        """Prepare environment for each test."""

        self.user_data = {'username': 'testuser', 'email': 'testuser@test.com',
                          'password': 'password123',
                          'confirm_password': 'password123'}
        user_response = requests.post(
            f"{self.BASE_URL}/signup/", json=self.user_data)
        self.assertEqual(user_response.status_code, 200)
        self.username = user_response.json().get('username')

        self.login_data = {'username': 'testuser', 'password': 'password123'}
        login_response = requests.post(
            f"{self.BASE_URL}/login/", data=self.login_data)
        self.token = login_response.json().get('access_token')
        self.headers = {'Authorization': f'Bearer {self.token}'}

        # Retrieve all users and find the ID for the created user
        response = requests.get(
            f"{self.BASE_URL}/users/", headers=self.headers)
        self.assertEqual(response.status_code, 200,
                         msg=f"Failed to retrieve users: {response.text}")
        users = response.json()
        user = next(
            (user for user in users if user['username'] == self.username),
            None)
        if user:
            self.user_id = user['id']
        else:
            raise ValueError("User not found")

        # Create a test post
        self.post_data = {'title': 'Test Post',
                          'content': 'This is a test post',
                          'user_id': self.user_id}
        post_response = requests.post(
            f"{self.BASE_URL}/posts/", json=self.post_data,
            headers=self.headers)
        self.post_id = post_response.json().get('id')
        self.assertEqual(post_response.status_code, 200)

        # Create a test comment
        self.comment_data = {'text': 'test comment'}
        comment_response = requests.post(
            f"{self.BASE_URL}/comments/{self.post_id}", headers=self.headers,
            json=self.comment_data)
        self.comment_id = comment_response.json().get('id')
        self.assertEqual(comment_response.status_code, 200)

    def tearDown(self):
        """Clean up after tests."""

        user_del_response = requests.delete(
            f"{self.BASE_URL}/users/{self.user_id}", headers=self.headers)
        self.assertEqual(user_del_response.status_code, 200)

    def test_read_all_comments(self):
        """Test retrieving all comments."""

        response = requests.get(
            f"{self.BASE_URL}/comments/", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_read_comment(self):
        """Test retrieving a comment by ID."""

        response = requests.get(
            f"{self.BASE_URL}/comments/{self.comment_id}",
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.comment_id)

    def test_update_comment(self):
        """Test updating a comment."""

        update_data = {'text': 'Updated Comment'}
        response = requests.put(
            f"{self.BASE_URL}/comments/{self.comment_id}", json=update_data,
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        updated_response = requests.get(
            f"{self.BASE_URL}/comments/{self.comment_id}",
            headers=self.headers)
        self.assertEqual(updated_response.json()['text'], 'Updated Comment')

    def test_delete_comment(self):
        """Test deleting a comment."""

        response = requests.delete(
            f"{self.BASE_URL}/comments/{self.comment_id}",
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        get_response = requests.get(
            f"{self.BASE_URL}/comments/{self.comment_id}",
            headers=self.headers)
        self.assertEqual(get_response.status_code, 404)
