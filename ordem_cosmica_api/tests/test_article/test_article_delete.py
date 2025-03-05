from rest_framework.test import APITestCase
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
class TestOrdemCosmicaAPIArticleDELETE(APITestCase, OrdemCosmicaAPIMixin):
    def test_user_must_send_jwt_to_delete(self):
        article = self.make_article()
        response = self.get_delete_response(self.get_article_detail_url(pk=article.pk))
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertEqual(
            response.data.get('detail'),
            "Authentication credentials were not provided."
        )

    def test_user_must_be_owner_to_delete(self):
        user_data_not_owner = {
            'username':'notonew',
            'password':'NotOwnerUser123'
        }
        self.make_author(username=user_data_not_owner.get('username'), password=user_data_not_owner.get('password'))
        access_token = self.get_user_token_pair(user_data=user_data_not_owner).get('access_token')
        article = self.make_article()
        response = self.get_delete_response(self.get_article_detail_url(pk=article.pk),access_token=access_token)
        self.assertEqual(
            response.status_code,
            403
        )
        self.assertEqual(
            response.data.get('detail'),
            'You do not have permission to perform this action.'
        )

    def test_user_owner_can_delete(self):
        user_data_owner = {
            'username':'notonew',
            'password':'NotOwnerUser123'
        }
        article = self.make_article(author_data=user_data_owner)
        access_token = self.get_user_token_pair(user_data=user_data_owner).get('access_token')
        response = self.get_delete_response(self.get_article_detail_url(pk=article.pk), access_token=access_token)
        self.assertEqual(
            response.status_code,
            204
        )
    