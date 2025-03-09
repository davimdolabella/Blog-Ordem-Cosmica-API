from rest_framework.test import APITestCase
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
class TestOrdemCosmicaAPIProfilePOST(APITestCase, OrdemCosmicaAPIMixin):
    def test_any_user_can_post_profile(self):
        response = self.get_post_response(self.get_profile_list_url(), data=self.default_user_data)
        self.assertEqual(
            response.status_code,
            201
        )

    def test_cannot_create_user_with_a_username_already_in_use(self):
        user_data = {
            'username':'test_user',
            'password':'TestUser123',
            'email':'emailteste@gmail.com'
        }
        self.make_author(username=user_data.get('username'), password=user_data.get('password'))
        response = self.get_post_response(self.get_profile_list_url(),data=user_data)
        self.assertEqual(
            response.status_code,
            400
        )
        self.assertIn('This username is already in use.', response.data.get('username'))

    def test_logged_user_cannot_create_another_user(self):
        user_data = {
            'username':'test_user',
            'password':'TestUser123',
            'email':'emailteste@gmail.com'
        }
        self.make_author(username=user_data.get('username'), password=user_data.get('password'))
        access_token = self.get_user_token_pair(user_data=user_data).get('access_token')
        response = self.get_post_response(self.get_profile_list_url(),data=user_data,access_token=access_token)
        self.assertEqual(
            response.status_code,
            403
        )

    def test_profile_fields_are_required(self):
        data = {}
        response = self.get_post_response(self.get_profile_list_url(), data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)