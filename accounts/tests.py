from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class StatusTests(TestCase):

    def test_pages(self):
        names = ['home', 'test', 'thanks', 'accounts:login', 'accounts:signup']
        for name in names:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

class OfflineTests(TestCase):

    def test_login_page(self):
        response = self.client.get(reverse('accounts:login'))

        # test that a user can login
        self.assertIn(b'<input id="id_username" maxlength="254" name="username" type="text"', response.content)
        self.assertIn(b'<input id="id_password" name="password" type="password">', response.content)
        self.assertIn(b'<button type="submit" name="_submit"', response.content)

        # test that a user can go to the sign up page from here
        self.assertIn(b'<a href="/accounts/signup/">', response.content)

    def test_signup_page(self):
        # test that a user can sign up
        response = self.client.get(reverse('accounts:signup'))

        self.assertIn(b'<input id="id_first_name"', response.content)
        self.assertIn(b'<input id="id_last_name"', response.content)
        self.assertIn(b'<input id="id_email"', response.content)
        self.assertIn(b'<input id="id_password1"', response.content)
        self.assertIn(b'<input id="id_password2"', response.content)
        self.assertIn(b'<button type="submit" name="_submit"', response.content)

        # test that a user can go to the login page from here
        self.assertIn(b'<a href="/accounts/login/">', response.content)
