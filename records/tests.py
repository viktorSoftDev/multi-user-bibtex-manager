from django.test import TestCase
from django.urls import reverse
# Create your tests here.



class StatusTests(TestCase):
    """
    Checking to see that the status codes are correct
    """

    def setUp(self):
        try:
            from populate import populate
            populate()
        except ImportError:
            print('The module populate does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function')

        from django.contrib.auth import get_user_model
        User = get_user_model()
        testuser =  User.objects.create_user('testuser', 'foo@example.com', 'pass')
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        pm = models.ProjectMember.objects.get_or_create(user=testuser, project=project, is_owner=True)

    def test_create_new_record(self):
        self.client.login(username='testuser', password='pass')
        names = ['projects:records:create',
                ]
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        for name in names:
            url = reverse(name, kwargs={'slug':project.slug})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, name)

    def test_record_specific_pages(self):
        self.client.login(username='testuser', password='pass')
        names = ['projects:records:single',
                'projects:records:edit',
                'projects:records:clone',
                ]
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        for name in names:
            url = reverse(name, kwargs={'slug':project.slug,'pk':3})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, name)

    def test_record_specific_pages_redirect(self):
        self.client.login(username='testuser', password='pass')
        names = ['projects:records:delete',
                ]
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        for name in names:
            url = reverse(name, kwargs={'slug':project.slug,'pk':3})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, name)


class RecordModelTests(TestCase):

    def setUp(self):
        try:
            from populate import populate
            populate()
        except ImportError:
            print('The module populate does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function')

        from django.contrib.auth import get_user_model
        User = get_user_model()
        testuser =  User.objects.create_user('testuser', 'foo@example.com', 'pass')
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        pm = models.ProjectMember.objects.get_or_create(user=testuser, project=project, is_owner=True)


    def test_number_of_records(self):
        from records import models
        r = models.Record.objects.all().count()
        self.assertEqual(10, r)

    def test_add_record(self):
        from records import models
        newRecord = models.Record(entry_type='article', cite_key='abc', title='newRecord')
        newRecord.save()
        r = models.Record.objects.all().count()
        self.assertEqual(11, r)

    def test_delete_record(self):
        from records import models
        someRecord = models.Record.objects.get(pk=3)
        someRecord.delete()
        r = models.Record.objects.all().count()
        self.assertEqual(9, r)


    def test_models_cascade(self):
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        from records import models
        r = models.Record.objects.all().count()
        self.assertEqual(10, r)
        project.delete()

        # testing to see that records get deleted as a project is deleted.
        r = models.Record.objects.all().count()
        self.assertEqual(0, r)



class CreateRecordViewTests(TestCase):
    
    def setUp(self):
        try:
            from populate import populate
            populate()
        except ImportError:
            print('The module populate does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function')

        from django.contrib.auth import get_user_model
        User = get_user_model()
        testuser =  User.objects.create_user(first_name='foo', last_name='bar', username='testuser', email='foo@example.com', password='pass')
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        pm = models.ProjectMember.objects.get_or_create(user=testuser, project=project, is_owner=True)

    def test_form_template(self):
        from projects import models

        self.client.login(username='testuser', password='pass')
        project = models.Project.objects.get(project_title="fake_title")
        response = self.client.get(reverse('projects:records:create',kwargs={'slug':project.slug}))

        # test to see that submit button is available and entry type can be chosen
        self.assertIn(b'<button type="submit" name="_submit"', response.content)
        self.assertIn(b'<select class="form_select" id="id_entry_type" name="entry_type">', response.content)
        # test to see that javascript is loaded.
        self.assertIn(b'<script type="text/javascript" src="/static/js/record_form.js"></script>', response.content)
