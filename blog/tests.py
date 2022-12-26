from django.contrib.auth.models import User
from django.test import TestCase, Client

from blog.models import Post, Comment


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", email="connor.s@skynet.com", password="12345"
        )
        # self.client.force_login(self.user)

        self.post = Post.objects.create(
            title='sometitle',
            text="someText",
            author=self.user)

    def test_profile(self):
        response = self.client.get("/profile/testuser")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(self.user.posts.all()), 1)

        self.assertIsInstance(self.user, User)

    def test_update_post(self):
        response = self.client.get(f'/profile/testuser/update/{self.post.slug}', follow=True)

        self.assertRedirects(response, f'/post/{self.post.slug}')

        self.client.force_login(self.user)
        response = self.client.get(f'/profile/testuser/update/{self.post.slug}')
        self.assertEqual(response.status_code, 200)


    def test_add_post(self):
        response = self.client.get('/create_post/')
        # self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/create_post/')


        self.client.force_login(self.user)
        response = self.client.get('/create_post/')
        self.assertEqual(response.status_code, 200)


    def test_add_comment(self):
        # response = self.client.post(f'/add_comment/{self.post.slug}', data={'text': 'myComment'})
        # self.assertRedirects(response, f'/login/')
        self.client.force_login(self.user)
        self.client.post(f'/add_comment/{self.post.slug}', data={'text': 'myComment'})

        self.assertEqual(Comment.objects.all().count(), 1)




