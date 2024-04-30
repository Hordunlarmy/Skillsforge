import unittest
import requests


class TestPOST(unittest.TestCase):
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

    def tearDown(self):
        """Clean up after tests."""

        user_del_response = requests.delete(
            f"{self.BASE_URL}/users/{self.user_id}", headers=self.headers)
        self.assertEqual(user_del_response.status_code, 200)

    def test_read_post(self):
        """Test retrieving a post by ID."""

        response = requests.get(
            f"{self.BASE_URL}/posts/{self.post_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.post_id)

    def test_update_post(self):
        """Test updating a post."""

        update_data = {'title': 'Updated Title', 'content': 'Updated content'}
        response = requests.put(
            f"{self.BASE_URL}/posts/{self.post_id}", json=update_data,
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        updated_response = requests.get(
            f"{self.BASE_URL}/posts/{self.post_id}", headers=self.headers)
        self.assertEqual(updated_response.json()['title'], 'Updated Title')

    def test_delete_post(self):
        """Test deleting a post."""

        response = requests.delete(
            f"{self.BASE_URL}/posts/{self.post_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        get_response = requests.get(
            f"{self.BASE_URL}/posts/{self.post_id}", headers=self.headers)
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
