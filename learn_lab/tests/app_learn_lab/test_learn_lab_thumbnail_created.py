import os

from django.conf import settings

from .test_learn_lab_base import LearnLabBaseTests


class ActivityThumbnailTests(LearnLabBaseTests):
    def setUp(self) -> None:
        self.activity = self.upload_file()
        return super().setUp()

    def tearDown(self) -> None:
        media_root = settings.MEDIA_ROOT
        pdf_path = f'{media_root}/learn_lab/files/test.pdf'
        image_path = f'{media_root}/learn_lab/thumbnails/test.png'

        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        if os.path.exists(image_path):
            os.remove(image_path)
        return super().tearDown()

    def test_saved_thumbnail(self):
        self.assertTrue(self.activity.thumbnail)

    def test_created_image(self):
        image_path = f'{settings.MEDIA_ROOT}/learn_lab/thumbnails/test.png'
        self.assertTrue(os.path.exists(image_path))
