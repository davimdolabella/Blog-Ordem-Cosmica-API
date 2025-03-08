from rest_framework.test import APITestCase
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
class TestOrdemCosmicaAPICommentPOST(APITestCase, OrdemCosmicaAPIMixin):

    def test_user_must_send_jwt_to_post_comment(self):
        response = self.get_post_response(self.get_comment_list_url())
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertEqual(
            response.data.get('detail'),
            "Authentication credentials were not provided."
        )

    def test_user_can_post_comment_with_correct_jwt_token(self):
        user_data = {
            'username':'test_user',
            'password':'TestUser123'
        }
        user = self.make_author(username=user_data.get('username'), password=user_data.get('password'))
        article = self.make_article(author_data=user, create_author=False)
        comment_data = {
            'content':'Um conteúdo',
            'user': user,
            'article': article.pk
        }
        access_token = self.get_user_token_pair(user_data=user_data).get('access_token')
        response = self.get_post_response(self.get_comment_list_url(),data=comment_data,access_token=access_token)
        self.assertEqual(
            response.status_code,
            201 #created 
        )

    def test_comment_fields_are_required(self):
        data = {}
        self.make_author(username=self.default_user_data.get('username'), password=self.default_user_data.get('password'))
        access_token = self.get_user_token_pair(user_data=self.default_user_data).get('access_token')
        response = self.get_post_response(self.get_comment_list_url(), data, access_token=access_token)
        self.assertEqual(response.status_code, 400)
        self.assertIn('content', response.data)
        self.assertIn('article', response.data)

    def test_comment_field_length_validation_on_post(self):
        comment_data = {
            'content': 'B' * 151, 
        }
        self.make_author(username=self.default_user_data.get('username'), password=self.default_user_data.get('password'))
        access_token = self.get_user_token_pair(user_data=self.default_user_data).get('access_token')
        response = self.get_post_response(self.get_comment_list_url(), data=comment_data, access_token=access_token)

        self.assertEqual(response.status_code, 400)
        self.assertIn('content', response.data)
    