from rest_framework.test import APITestCase
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
from unittest.mock import patch
class TestOrdemCosmicaAPIArticleGET(APITestCase, OrdemCosmicaAPIMixin):
    def test_article_list_returns_empty(self):
        response = self.get_get_response(self.get_article_list_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_article_list_returns_status_code_200(self):
        response = self.get_get_response(self.get_article_list_url())
        self.assertEqual(
            response.status_code, 200
        )

    @patch('ordem_cosmica_api.views.OrdemCosmicaAPIPagination.page_size', new=2)
    def test_article_list_returns_correct_pagination(self):
        self.make_article_in_batch(qtd=4)
        response_page1 = self.get_get_response(self.get_article_list_url())
        response_page2 = self.get_get_response(self.get_article_list_url() + '?page=2')
        # 4 articles were created
        self.assertEqual(
            response_page1.data.get('count'), 4
        )
        # 2 articles are shown, because of the pagination
        self.assertEqual(
            len(response_page1.data.get('results')),
            2
        )
        # 2 articles are shown, because of the pagination
        self.assertEqual(
            len(response_page2.data.get('results')),
            2
        )

    def test_article_detail_return_status_200(self):
        article = self.make_article()
        response = self.get_get_response(self.get_article_detail_url(pk=article.pk))
        self.assertEqual(
            response.status_code,
            200
        )