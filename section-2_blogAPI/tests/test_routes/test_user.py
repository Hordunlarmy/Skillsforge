import unittest
import requests


class TestUSER(unittest.TestCase):
    BASE_URL = "http://localhost:8000"

    def test_get_users(self):
        """ Test Create A User Account ."""

        self.user_data = {'username': 'testuser1',
                          'email': 'testuser1@test.com',
                          'password': 'password123',
                          'confirm_password': 'password123'}
        user_response = requests.post(
            f"{self.BASE_URL}/signup/", json=self.user_data)
        self.assertEqual(user_response.status_code, 200)
        self.username = user_response.json().get('username')

        self.login_data = {'username': 'testuser1', 'password': 'password123'}
        login_response = requests.post(
            f"{self.BASE_URL}/login/", data=self.login_data)
        self.token = login_response.json().get('access_token')
        self.headers = {'Authorization': f'Bearer {self.token}'}

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

        """ Test Retrieve all users """

        response = requests.get(
            f"{self.BASE_URL}/users/", headers=self.headers)
        self.assertEqual(response.status_code, 200,
                         msg=f"Failed to retrieve users: {response.text}")

        """ Test Delete A User """

        user_del_response = requests.delete(
            f"{self.BASE_URL}/users/{self.user_id}", headers=self.headers)
        self.assertEqual(user_del_response.status_code, 200)
