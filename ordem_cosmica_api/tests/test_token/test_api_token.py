from rest_framework.test import APITestCase
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
class TestAPIToken(APITestCase, OrdemCosmicaAPIMixin):
    def test_user_need_credentials_to_obtain_pair_token(self):
        data ={}
        response = self.get_user_token_pair(data)
        self.assertEqual(
            response.get('response').status_code,
            400
        )
        self.assertIn('username', response.get('response').data)
        self.assertIn('password', response.get('response').data)
    
    def test_user_need_to_send_correct_credentials_to_obtain_pair_token(self):
        data = {
            'username': 'username',
            'password': 'Pass123'
        }
        response = self.get_user_token_pair(data)
        self.assertEqual(
            response.get('response').status_code,
            401
        )
        self.assertIn('No active account found with the given credentials', response.get('response').data.get('detail'))
    
    def test_user_can_obtain_pair_token_with_correct_credentials(self):
        data = {
            'username': 'username',
            'password' : 'Pass123'
        }
        self.make_author(**data)
        response = self.get_user_token_pair(data)
        self.assertEqual(
            response.get('response').status_code,
            200
        )

    def test_user_must_send_jwt_to_refresh(self):
        data = {
            'username': 'username',
            'password' : 'Pass123'
        }
        self.make_author(**data)
        response = self.get_user_new_access_token()
        self.assertEqual(
            response.get('response').status_code,
            400
        )
        self.assertIn(
            'This field may not be blank.',
            response.get('response').data.get('refresh')
        )

    def test_user_must_send_correct_jwt_to_refresh(self):
        data = {
            'username': 'username',
            'password' : 'Pass123'
        }
        self.make_author(**data)
        response = self.get_user_new_access_token(refresh_token="invalid_token")
        self.assertEqual(
            response.get('response').status_code,
            401
        )
        self.assertIn(
            'Token is invalid or expired',
            response.get('response').data.get('detail')
        )

    def test_user_can_refresh_with_correct_jwt(self):
        data = {
            'username': 'username',
            'password' : 'Pass123'
        }
        self.make_author(**data)
        refresh_token = self.get_user_token_pair(data).get('refresh_token')
        response = self.get_user_new_access_token(refresh_token=refresh_token)
        self.assertEqual(
            response.get('response').status_code,
            200
        )

    def test_verify_with_invalid_token(self):
        response = self.get_post_response(self.get_token_verify_url(), data={'token':'invalid_token'})
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertIn(
            'Token is invalid or expired',
            response.data.get('detail')
        )
    
    def test_verify_with_correct_access_and_refresh_token(self):
        data = {
            'username':'username',
            'password':'Pass123'
        }
        self.make_author(**data)
        tokens = self.get_user_token_pair(data)
        response_access = self.get_post_response(self.get_token_verify_url(), data={'token':tokens.get('access_token')})
        response_refresh = self.get_post_response(self.get_token_verify_url(), data={'token':tokens.get('refresh_token')})
        self.assertEqual(
            response_access.status_code,
            200
        )
        self.assertEqual(
            response_refresh.status_code,
            200
        )