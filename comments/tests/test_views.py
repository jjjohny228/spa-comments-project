import io
import os
import tempfile
from http import HTTPStatus
from shutil import rmtree

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from django_dynamic_fixture import G
from PIL import Image

from accounts.models import User
from labels.models import Label
from releases.models import Release
from releases.models import TradeInfo

# Create a temporary file directory for testing
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class LabelCreateViewTest(TestCase):
    """
    This class test LabelCreateView.
    It uses django_dynamic_fixture to generate User and Label objects.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = G(User)
        cls.url = reverse('labels:create')

    def setUp(self):
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_GET_it_returns_status_code_200(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_GET_it_contain_right_text(self):
        self.assertContains(self.response, 'Enter label info')

    def test_GET_it_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'labels/add_label.html')

    def test_POST_it_handles_success_request(self):
        post_response = self.client.post(
            self.url,
            {'name': 'Test Label', 'description': 'Test Description'},
            user=self.user,
        )
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Label.objects.filter(name='Test Label').count(), 1)
        self.assertEqual(post_response.url, reverse('labels:my-labels'))

    def test_POST_it_returns_error_if_similarly_named_label_already_exists_for_given_user(
        self,
    ):
        Label.objects.create(name='Test Label', description='Test Description', owner=self.user)

        # creating the same label
        response = self.client.post(self.url, {'name': 'Test Label', 'description': 'Another Description'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Label name is not unique.')

    def test_GET_it_redirects_logged_out_user(self):
        self.client.logout()
        get_response = self.client.get(self.url)
        self.assertRedirects(get_response, reverse('account_login') + '?next=' + self.url)

    def test_POST_it_redirects_logged_out_user(self):
        self.client.logout()
        post_response = self.client.post(self.url, {'name': 'Test Label', 'description': 'Test Description'})
        self.assertRedirects(post_response, reverse('account_login') + '?next=' + self.url)

    @classmethod
    def tearDown(cls):
        """
        Clean up files after each test.
        """
        rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDown(cls)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class LabelListViewTest(TestCase):
    """
    This class tests pagination and labels listing per page and LabelListView.
    It uses django_dynamic_fixture to generate User and Label objects.
    """

    @classmethod
    def setUpTestData(cls):
        image = Image.new('RGB', (150, 150), color='red')
        # Save the image to a BytesIO buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='JPEG')
        # Create a SimpleUploadedFile from the buffer
        logo = SimpleUploadedFile('test_image.jpg', image_buffer.getvalue())
        G(Label, logo=logo, n=30)
        cls.url = reverse('labels:list')
        cls.user = G(User)

    def setUp(self):
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_GET_it_returns_valid_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_GET_it_uses_right_template(self):
        self.assertTemplateUsed('labels/all_labels.html')

    def test_GET_it_redirects_logged_out_user(self):
        self.client.logout()
        get_response = self.client.get(self.url)
        # Check that it redirects to login page
        self.assertRedirects(get_response, reverse('account_login') + '?next=' + self.url)

    def test_GET_it_uses_pagination(self):
        self.assertTrue('is_paginated' in self.response.context)
        self.assertTrue(self.response.context['is_paginated'])

    def test_GET_it_returns_right_objects_number_per_page(self):
        self.assertEqual(len(self.response.context['labels']), settings.DEFAULT_PAGE_SIZE)

    def test_GET_it_returns_error_page_when_labels_page_is_out_of_range(self):
        invalid_response = self.client.get(self.url + f'?page={5}')
        self.assertTemplateUsed(invalid_response, 'common/errors/pages_misc_error.html')

    def test_GET_it_contains_right_text_if_there_are_no_labels(self):
        Label.objects.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, 'There are no labels so far.')

    def test_GET_contains_correct_logo_thumbnail_resolution(self):
        labels = self.response.context['labels']
        for label in labels:
            # Check if label's thumbnail URL contains correct resolution
            self.assertIn(str(label.logo_thumbnail.width), self.response.content.decode())
            self.assertIn(str(label.logo_thumbnail.height), self.response.content.decode())

    @classmethod
    def tearDown(cls):
        """
        Clean up files after each test.
        """
        rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDown(cls)
