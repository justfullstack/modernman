
from django.core.management.base import BaseCommand
from collections import Counter
import csv
import os.path
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from shop import models


class Command(BaseCommand):
    help = 'Import products in ModernMan fixtures'

    def add_arguments(self, parser):
        '''imports products
        usage: import_data path/to/csvfile path/to/image_basedir'''
        parser.add_argument('csvfile', type=open)
        parser.add_argument('image_basedir', type=str)

    # required : command logic goes here
    def handle(self, *args, **options):

        self.stdout.write("Importing products...")

        counter = Counter()
        reader = csv.DictReader(options.pop('csvfile'))

        for row in reader:
            product, created = models.Product.objects.get_or_create(
                name=row["name"],
                price=row["price"]
            )

            product.description = row["description"]
            product.slug = slugify(row["name"])

            for imported_tag in row["tags"].split('|'):
                tag, tag_created = models.ProductTag.object.get_or_create(
                    name=imported_tag)
                product.tags.add(tag)
                counter['tags'] += 1

                if tag_created:
                    counter['tags_created'] += 1

            with open(os.path.join(options['image_basedir'], row['image_filename']), 'rb') as file:
                image = models.ProductImage(
                    product=product,
                    image=ImageFile(file,
                                    name=row['image_filename']
                                    )
                )
                image.save()
                counter['iamges'] = + 1

                if created:
                    counter['products_created'] = + 1
                    self.stdout.write(
                        f"{counter['products']} products processed...")
                    self.stdout.write(
                        f"{counter['created']} products created...")
                    self.stdout.write(f"{counter['tags']} tags processed...")
                    self.stdout.write(
                        f"{counter['tags_created']} tags created...")
                    self.stdout.write(f"{counter['images']} images created...")
