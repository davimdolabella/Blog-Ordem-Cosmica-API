from rest_framework.test import APITestCase
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
class TestOrdemCosmicaAPIArticlePOST(APITestCase, OrdemCosmicaAPIMixin):
    def test_user_must_send_jwt_to_post(self):
        response = self.get_post_response(self.get_article_list_url())
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertEqual(
            response.data.get('detail'),
            "Authentication credentials were not provided."
        )

    def test_user_can_post_with_correct_jwt_token(self):
        user_data = {
            'username':'test_user',
            'password':'TestUser123'
        }
        user = self.make_author(username=user_data.get('username'), password=user_data.get('password'))
        article_data = {
            'title':'Um Título',
            'description': 'Uma descrição',
            'content':'Um conteúdo',
            'user': user
        }
        access_token = self.get_user_token_pair(user_data=user_data).get('access_token')
        response = self.get_post_response(self.get_article_list_url(),data=article_data,access_token=access_token)
        self.assertEqual(
            response.status_code,
            201 #created 
        )

    def test_article_fields_are_required_on_post(self):
        data = {}
        self.make_author(username=self.default_user_data.get('username'), password=self.default_user_data.get('password'))
        access_token = self.get_user_token_pair(user_data=self.default_user_data).get('access_token')
        response = self.get_post_response(self.get_article_list_url(), data, access_token=access_token)
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)
        self.assertIn('content', response.data)

    def test_article_field_length_validation_on_post(self):
        article_data = {
            'title': 'A' * 61, 
            'description': 'B' * 151, 
            'content': 'Conteúdo válido'
        }
        self.make_author(username=self.default_user_data.get('username'), password=self.default_user_data.get('password'))
        access_token = self.get_user_token_pair(user_data=self.default_user_data).get('access_token')
        response = self.get_post_response(self.get_article_list_url(), data=article_data, access_token=access_token)

        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)


    