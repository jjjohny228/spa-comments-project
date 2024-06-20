import os
import tempfile
from shutil import rmtree

from ddf import G
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import ValidationError
from django.test import TestCase
from django.test import override_settings

from comments.models import Comment
from comments.validators import validate_username, validate_file_type, validate_file_size

# Create a temporary file directory for testing
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CommentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.label = G(Comment, author='author1', text='Test comment')

    def test_str_method(self):
        self.assertEqual(str(self.label), 'Test comment')

    def test_it_asserts_validation_error_if_file_format_is_incorrect(self):
        invalid_file = SimpleUploadedFile('test_video.mov', b'test', content_type='video/mov')
        invalid_label = G(Comment, file=invalid_file)
        with self.assertRaises(ValidationError) as error:
            invalid_label.full_clean()
            expected_error_message = 'Invalid file type.'
            self.assertEqual(error.exception.message, expected_error_message)

    def test_it_asserts_validation_error_if_file_size_is_too_big(self):
        invalid_file = SimpleUploadedFile('test.txt', b'test some bytes' * 1024 * 101, content_type='text/plain')
        invalid_label = G(Comment, file=invalid_file)
        with self.assertRaises(ValidationError) as error:
            invalid_label.full_clean()
            expected_error_message = 'File size must be less than 100KB.'
            self.assertEqual(error.exception.message, expected_error_message)

    def test_it_asserts_validation_error_if_username_is_invalid(self):
        invalid_label = G(Comment, author='(s98р')
        with self.assertRaises(ValidationError) as error:
            invalid_label.full_clean()
            expected_error_message = 'User Name can only contain letters and digits from the Latin alphabet.'
            self.assertEqual(error.exception.message, expected_error_message)

    @classmethod
    def tearDown(cls):
        """
        Clean up files after each test.
        """
        rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDown(cls)
