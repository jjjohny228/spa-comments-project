import os
import tempfile

from http import HTTPStatus
from shutil import rmtree
from captcha.models import CaptchaStore

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from django_dynamic_fixture import G

from comments.models import Comment

# Create a temporary file directory for testing
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CommentListViewTest(TestCase):
    """
    This class tests pagination and comments listing per page and CommentListView.
    It uses django_dynamic_fixture to generate User and Comment objects.
    """

    @classmethod
    def setUpTestData(cls):
        [G(Comment, level=0) for _ in range(30)]
        cls.url = reverse('comments:all')

    def setUp(self):
        self.response = self.client.get(self.url)

    def test_GET_it_returns_valid_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_GET_it_uses_right_template(self):
        self.assertTemplateUsed('comments/all_comments.html')

    def test_GET_it_uses_pagination(self):
        self.assertTrue('is_paginated' in self.response.context)
        self.assertTrue(self.response.context['is_paginated'])

    def test_GET_it_returns_right_objects_number_per_page(self):
        self.assertEqual(len(self.response.context['comments']), settings.DEFAULT_PAGE_SIZE)

    def test_GET_it_returns_error_page_when_comments_page_is_out_of_range(self):
        invalid_response = self.client.get(self.url + f'?page={5}')
        self.assertTemplateUsed(invalid_response, 'common/errors/pages_error.html')

    def test_GET_it_contains_right_text_if_there_are_no_comments(self):
        Comment.objects.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, 'There are no comments yet...')

    @classmethod
    def tearDown(cls):
        """
        Clean up files after each test.
        """
        rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDown(cls)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CommentViewTest(TestCase):
    """
    This class test LabelCreateView.
    It uses django_dynamic_fixture to generate User and Comment objects.

    """
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('comments:add')
        cls.comment_image = SimpleUploadedFile('image.jpg', b'image content', content_type='image/jpeg')
        # Get a CAPTCHA challenge
        cls.captcha_key = CaptchaStore.generate_key()
        cls.captcha_value = CaptchaStore.objects.get(hashkey=cls.captcha_key).response
        cls.data = {
                'author': 'user',
                'email': 'some1@gmail.com',
                'homepage': 'https://example.com',
                'text': 'Test text',
                'file': cls.comment_image,
                'captcha_0': cls.captcha_key,
                'captcha_1': cls.captcha_value,
            }

    def test_POST_it_handles_success_request(self):
        post_response = self.client.post(self.url, self.data)
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Comment.objects.filter(author='user').count(), 1)
        self.assertEqual(post_response.url, reverse('comments:all'))

    def test_POST_it_returns_error_if_username_is_incorrect(self):
        invalid_data = {
            'author': 'user[]',
            'email': 'some1@gmail.com',
            'homepage': 'https://example.com',
            'text': 'Test text',
            'file': self.comment_image,
            'captcha_0': self.captcha_key,
            'captcha_1': self.captcha_value,
        }

        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'User Name can only contain letters and digits from the Latin alphabet.')

    def test_POST_it_returns_error_if_captcha_is_incorrect(self):
        invalid_data = {
            'author': 'user',
            'email': 'some1@gmail.com',
            'homepage': 'https://example.com',
            'text': 'Test text',
            'file': self.comment_image,
            'captcha_0': self.captcha_key,
            'captcha_1': 'false',
        }

        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Invalid CAPTCHA')

    def test_POST_it_returns_error_if_file_type_is_incorrect(self):
        invalid_file = SimpleUploadedFile('test_video.mov', b'test', content_type='video/mov')
        invalid_data = {
            'author': 'user',
            'email': 'some1@gmail.com',
            'homepage': 'https://example.com',
            'text': 'Test text',
            'file': invalid_file,
            'captcha_0': self.captcha_key,
            'captcha_1': self.captcha_value,
        }

        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Invalid file type.')

    @classmethod
    def tearDown(cls):
        """
        Clean up files after each test.
        """
        rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDown(cls)