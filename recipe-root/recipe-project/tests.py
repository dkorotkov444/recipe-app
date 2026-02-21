# recipe_project/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class GlobalAuthTests(TestCase):
    def setUp(self):
        # Create a user for login/logout testing
        self.username = 'chef_user'
        self.password = 'securepassword123'
        self.user = User.objects.create_user(
            username=self.username, 
            password=self.password
        )

    # 1. Test Login Logic
    def test_login_view_success(self):
        """Test the project-level login logic redirects correctly."""
        url = reverse('login')
        response = self.client.post(url, {
            'username': self.username,
            'password': self.password
        })
        # Successful login should redirect to the recipe list
        self.assertRedirects(response, reverse('recipes:recipes_list'))

    # 2. Test Logout and Session Clearing
    def test_logout_redirection_and_session_clear(self):
        """Verify hitting logout clears session and redirects to success page."""
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get(reverse('logout'))
        # Should redirect to logout-success
        self.assertRedirects(response, reverse('logout_success'))
        self.assertNotIn('_auth_user_id', self.client.session)

    # 3. Test Logout Success Page
    def test_logout_success_view_uses_correct_template(self):
        """Verify the logout success page renders global template."""
        response = self.client.get(reverse('logout_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout_success.html')

    # 4. Test Global Protection (The Gatekeeper)
    def test_view_redirects_unauthenticated_user(self):
        """Ensure guests are redirected from protected views to login."""
        # Test against the recipe list which is now protected
        url = reverse('recipes:recipes_list')
        response = self.client.get(url)
        # Should result in a redirect
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)