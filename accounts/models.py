from django.db import models
from customauth.models import CustomUser

############################ SHIPPING ############################################


# address
COUNTIES = (
    ("001", "Mombasa"),
    ("002", "Kwale"),
    ("003", "Kilifi"),
    ("004", "Tana River"),
    ("005", "Lamu"),
    ("006", "Taita Taveta"),
    ("007", "Garissa"),
    ("008", "Wajir"),
    ("009", "Mandera"),
    ("010", "Marsabit"),
    ("011", "Isiolo"),
    ("012", "Meru"),
    ("013", "Tharaka-Nithi"),
    ("014", "Embu"),
    ("015", "Kitui"),
    ("016", "Machakos"),
    ("017", "Makueni"),
    ("018", "Nyandarua"),
    ("019", "Nyeri"),
    ("020", "Kirinyaga"),
    ("021", "Murang'a"),
    ("022", "Kiambu"),
    ("023", "Turkana"),
    ("024", "West Pokot"),
    ("025", "Samburu"),
    ("026", "Trans-Nzoia"),
    ("027", "Uasin Gishu"),
    ("028", "Elgeyo-Marakwet"),
    ("029", "Nandi"),
    ("030", "Baringo"),
    ("031", "Laikipia"),
    ("032", "Nakuru"),
    ("033", "Narok"),
    ("034", "Kajiado"),
    ("035", "Kericho"),
    ("036", "Bomet"),
    ("037", "Kakamega"),
    ("038", "Vihiga"),
    ("039", "Bungoma"),
    ("040", "Busia"),
    ("041", "Siaya"),
    ("042", "Kisumu"),
    ("043", "Homa Bay"),
    ("044", "Migori"),
    ("045", "Kisii"),
    ("046", "Nyamira"),
    ("047", "Nairobi")
)


CITIES = (
    ("MBS", "Mombasa"),
    ("NBI", "Nairobi"),
    ("KSM", "Kisumu"),
    ("NKR", "Nakuru")
)

COUNTRIES = (
    ("KE", "Kenya"),
)

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.')
)


class Address(models.Model):

    class Meta:
        verbose_name_plural = 'Addresses'

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=3,
        choices=TITLE_CHOICES
    )

    name = models.CharField(
        'name',
        max_length=60,
        null=False,
        blank=False
    )

    address = models.CharField(
        "Address",
        max_length=60,
        null=False,
        blank=False
    )

    postal_code = models.CharField(
        "Postal Code",
        max_length=12,
        null=True,
        blank=True
    )

    town = models.CharField(
        'town',
        max_length=60,
        null=False,
        blank=False)

    county = models.CharField(
        'county',
        max_length=3,
        choices=COUNTIES,
        null=False,
        blank=False
    )

    city = models.CharField(
        'city',
        max_length=60,
        choices=CITIES,
        null=True,
        blank=True
    )

    country = models.CharField(
        'county',
        max_length=3,
        choices=COUNTRIES,
        default='KE'
    )

    phone_no = models.IntegerField(default=000)

    def __str__(self):
        return f"{self.title}. {self.name},\n{self.address} - {self.postal_code},\n{self.town}, \n{self.county}, \n{self.city},  \n{self.country}, \n{self.phone_no}"
