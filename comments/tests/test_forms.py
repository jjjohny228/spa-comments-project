import os
import tempfile

from captcha.models import CaptchaStore
from shutil import rmtree

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from comments.forms import CommentForm

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CommentFormTest(TestCase):
    """
    Test case for the CommentForm.

    """

    @classmethod
    def setUpTestData(cls):
        # Create a data for testing
        # Create a Comment object for testing
        cls.comment_image = SimpleUploadedFile('image.jpg', b'image content', content_type='image/jpeg')
        # Get a CAPTCHA challenge
        cls.captcha_key = CaptchaStore.generate_key()
        cls.captcha_value = CaptchaStore.objects.get(hashkey=cls.captcha_key).response
        cls.form = CommentForm

    def test_it_is_valid_if_valid_data_is_provided(self):
        form_data = {
            'author': 'user',
            'email': 'some1@gmail.com',
            'homepage': 'https://example.com',
            'text': 'Test text',
            'file': self.comment_image,
            'captcha_0': self.captcha_key,
            'captcha_1': self.captcha_value,
        }
        # populate the form with valid form data
        form = self.form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_it_is_valid_if_form_data_without_file_is_valid(self):
        form_data_no_file = {
            'author': 'user',
            'email': 'some1@gmail.com',
            'homepage': 'https://example.com',
            'text': 'Test text',
            'captcha_0': self.captcha_key,
            'captcha_1': self.captcha_value,
        }
        valid_form = self.form(data=form_data_no_file)
        self.assertTrue(valid_form.is_valid())

    def test_it_is_invalid_if_captcha_is_invalid(self):
        # populate the form with invalid form data
        invalid_data = {
            'author': 'user',
            'email': 'some1@gmail.com',
            'homepage': 'https://example.com',
            'text': 'Test text',
            'captcha_0': self.captcha_key,
            'captcha_1': 'not right',
        }
        form = self.form(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_it_saves_the_comment(self):
        form_data = {
            'author': 'user',
            'email': 'some1@gmail.com',
            'homepage': 'https://example.com',
            'text': 'Test text',
            'file': self.comment_image,
            'captcha_0': self.captcha_key,
            'captcha_1': self.captcha_value,
        }
        # Test form save method
        form = self.form(data=form_data)
        release = form.save()
        self.assertEqual(release.text, 'Test text')

    def test_it_has_help_text_in_user_field(self):
        form = CommentForm()
        expected_help_text = 'This value may contain only letters, numbers'
        self.assertEqual(form.fields['author'].help_text, expected_help_text)

    def test_it_returns_form_error_for_invalid_username(self):
        invalid_form_data = {
            'author': '()тще',
            'email': 'some1@gmail.com',
            'homepage': 'https://example.com',
            'text': 'Test text',
            'file': self.comment_image,
            'captcha_0': self.captcha_key,
            'captcha_1': self.captcha_value,
        }
        form = self.form(data=invalid_form_data)
        exception_text = 'User Name can only contain letters and digits from the Latin alphabet.'
        self.assertFalse(form.is_valid())
        self.assertIn(exception_text, form.errors['author'])

    @classmethod
    def tearDown(cls):
        """
        Clean up files after each test.
        """
        rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDown(cls)

    # def test_it_returns_form_error_for_big_text_file(self):
    #     # Create a file content that exceeds 100 KB
    #     invalid_file = SimpleUploadedFile('test.txt', b'test some bytes' * 1024 * 101, content_type='text/plain')
    #     invalid_form_data = {
    #         'author': 'test1author',
    #         'email': 'some1@gmail.com',
    #         'homepage': 'https://example.com',
    #         'text': 'Test text',
    #         'file': invalid_file,
    #         'captcha_0': self.captcha_key,
    #         'captcha_1': self.captcha_value,
    #     }
    #     form = self.form(data=invalid_form_data)
    #     exception_text = 'File size must be less than 100KB.'
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(exception_text, form.errors['file'])
    #
    # def test_it_returns_form_error_for_invalid_file_type(self):
    #     # Create a file content that exceeds 100 KB
    #     invalid_file = SimpleUploadedFile('test_video.mov', b'test', content_type='video/mov')
    #     invalid_form_data = {
    #         'author': 'test1author',
    #         'email': 'some1@gmail.com',
    #         'homepage': 'https://example.com',
    #         'text': 'Test text',
    #         'file': invalid_file,
    #         'captcha_0': self.captcha_key,
    #         'captcha_1': self.captcha_value,
    #     }
    #     form = self.form(data=invalid_form_data)
    #     exception_text = 'File size must be less than 100KB.'
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(exception_text, form.errors['file'])