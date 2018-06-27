import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mubm.settings')

import django
django.setup()

## FAKE POP SCRIPT
import random
from projects.models import Project
from accounts.models import User
from records import record

from faker import Faker

fakegen = Faker()

entry_types =   ['article',
                'book',
                'mastersthesis',
                'conference']

def add_user():
    name = fakegen.name().split()
    fakefname = name[0]
    fakesname = name[1]
    fakeemail = fakegen.email()
    fakepass = fakegen.word(ext_word_list=None)
    u = User.objects.get_or_create(username=fakeemail, email = fakeemail, first_name=fakefname, last_name=fakesname, password=fakepass)[0]
    u.save()
    return u

def add_project():
    fake_title = fakegen.text(max_nb_chars=50, ext_word_list=None)
    p = Project.objects.get_or_create(project_title=fake_title)[0]

    p.save()
    return p

def add_record():
    fake_type = random.choice(entry_types)
    fake_key = fakegen.word(ext_word_list=None)
    fake_title = fakegen.text(max_nb_chars=150, ext_word_list=None)
    fake_year = fakegen.year()

    r = Record.objects.get_or_create(entry_type=fake_type, cite_key=fake_key,
                                    title=fake_title, year=fake_year)[0]

    r.save()


    return r

def populate(N=10):
    for entry in range(N):
        user = add_user()
        for i in range(2):
            project = add_project()
            project.save()
            project.users.add(user)
            project.save()
            for j in range(5):
                record = add_record()
                record.users = user
                record.project = project
                record.save()

if __name__ == '__main__':
    print("populating database...")
    populate()
    print("population complete!")
