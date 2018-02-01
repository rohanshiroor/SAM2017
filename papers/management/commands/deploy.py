import csv

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from papers.models import Author, PCM, PCC, Admin

STREET_LINE_1 = 5
STREET_LINE_2 = 6
CITY = 7
STATE = 8
ZIP_CODE = 9

USERNAME = 0
FIRST_NAME = 1
LAST_NAME = 2
PHONE_NUMBER = 3
PASSWORD = 4

TITLE = 1
ABSTRACT = 2
AUTHOR_ID = 3
VERSION = 4
PCM_ONE = 5
PCM_TWO = 6
PCM_THREE = 7


class Command(BaseCommand):
    help = "Setup database"

    def handle(self, *args, **options):
        with open("data/authors.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Author.objects.get_or_create(
                    username=row[USERNAME],
                    first_name=row[FIRST_NAME],
                    last_name=row[LAST_NAME],
                    phone_number=row[PHONE_NUMBER],
                    user_type=0,
                    password=make_password(row[PASSWORD]),
                    street_line_1=row[STREET_LINE_1],
                    street_line_2=row[STREET_LINE_2],
                    city=row[CITY],
                    state=row[STATE],
                    zip_code=row[ZIP_CODE]
                )

        with open("data/pcm.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = PCM.objects.get_or_create(
                    username=row[USERNAME],
                    first_name=row[FIRST_NAME],
                    last_name=row[LAST_NAME],
                    phone_number=row[PHONE_NUMBER],
                    user_type=1,
                    password=make_password(row[PASSWORD]),
                    street_line_1=row[STREET_LINE_1],
                    street_line_2=row[STREET_LINE_2],
                    city=row[CITY],
                    state=row[STATE],
                    zip_code=row[ZIP_CODE]
                )

        with open("data/pcc.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = PCC.objects.get_or_create(
                    username=row[USERNAME],
                    first_name=row[FIRST_NAME],
                    last_name=row[LAST_NAME],
                    phone_number=row[PHONE_NUMBER],
                    user_type=2,
                    password=make_password(row[PASSWORD]),
                    street_line_1=row[STREET_LINE_1],
                    street_line_2=row[STREET_LINE_2],
                    city=row[CITY],
                    state=row[STATE],
                    zip_code=row[ZIP_CODE]
                )

        with open("data/admin.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Admin.objects.get_or_create(
                    username=row[USERNAME],
                    first_name=row[FIRST_NAME],
                    last_name=row[LAST_NAME],
                    phone_number=row[PHONE_NUMBER],
                    user_type=3,
                    password=make_password(row[PASSWORD]),
                    street_line_1=row[STREET_LINE_1],
                    street_line_2=row[STREET_LINE_2],
                    city=row[CITY],
                    state=row[STATE],
                    zip_code=row[ZIP_CODE]
                )
'''
        with open("data/papers.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Paper.objects.get_or_create(
                    # file=get_file
                    title = row[TITLE],
                    abstract = row[ABSTRACT],
                    author = row[AUTHOR_ID],
                    submission_date = row[1],
                    version = row[VERSION],
                    pcm_one = row[PCM_ONE],
                    pcm_two = row[PCM_TWO],
                    pcm_three = row[PCM_THREE],
                )
'''

