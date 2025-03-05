from django.test import TestCase
from ordem_cosmica_api.models import Article, Profile, User


class OrdemCosmicaAPIMixin:
    def make_author(
        self,
        username='username',
        password='123456',
        email='username@email.com',
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        return Profile.objects.create(
            user = user
        )

    def make_article(
        self,
        author_data=None,
        title='Article Title',
        description='Recipe Description',
        content='Article Content',
    ):
        if author_data is None:
            author_data = {}

        return Article.objects.create(
            author=self.make_author(**author_data),
            title=title,
            description=description,
            content=content
        )

    def make_article_in_batch(self, qtd=10):
        articles = []
        for i in range(qtd):
            kwargs = {
                'title': f'Article Title {i}',
                'author_data': {'username': f'u{i}'}
            }
            article = self.make_article(**kwargs)
            articles.append(article)
        return articles


class OrdemCosmicaAPITestBase(TestCase, OrdemCosmicaAPIMixin):
    def setUp(self) -> None:
        return super().setUp()
