from io import StringIO
import tempfile
from django.core.management import call_command
from django.test import TestCase, override_settings
from shop import models


class TestImport(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def testImportData(self):
        # test for the csv file to exist,
        # test images to be present in the basedir
        out = StringIO()
        args = ['core/fixtures/test/product-sample.csv',
                'core/fixtures/test/product-sampleimages/']
        # Django offers the function call_command() to invoke management commands from Python itself
        call_command('import_data', *args, stdout=out)

        expected_out = ("Importing products\n"
                        "Products processed=3 (created=3)\n"
                        "Tags processed=6 (created=6)\n"
                        "Images processed=3\n")
        self.assertEqual(out.getvalue(), expected_out)
        self.assertEqual(models.Product.objects.count(), 3)
        self.assertEqual(models.ProductTag.objects.count(), 6)
        self.assertEqual(models.ProductImage.objects.count(), 3)
