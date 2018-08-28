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


    def test_no_slug_project_pages(self):
        self.client.login(username='testuser', password='pass')
        names = ['projects:all',
                'projects:create',
                ]

        for name in names:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_slug_specific_projects(self):
        self.client.login(username='testuser', password='pass')
        names = ['projects:single',
                'projects:invite',
                'projects:settings',
                'projects:edit',
                'projects:import',
                'projects:export',
                ]

        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        for name in names:
            url = reverse(name, kwargs={'slug':project.slug})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, name)

    def test_slug_specific_projects_redirect(self):
        self.client.login(username='testuser', password='pass')
        names = ['projects:leave',
                ]

        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        for name in names:
            url = reverse(name, kwargs={'slug':project.slug})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, name)


class LoginContentTests(TestCase):
    """
    Test that user can see the logged in content
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
        testuser =  User.objects.create_user(first_name='foo', last_name='bar', username='testuser', email='foo@example.com', password='pass')
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        pm = models.ProjectMember.objects.get_or_create(user=testuser, project=project, is_owner=True)

    def test_list_exists(self):

        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('projects:all'))

        # See that user can log out, access the project list and that the users' name is present
        self.assertIn(b'<a href="/accounts/logout/">Log out</a>', response.content)
        self.assertIn(b'<a href="/projects/">My Projects</a>', response.content)
        self.assertIn(b'foo bar', response.content)
        # see that there is an image present (sidenav)
        self.assertIn(b'img', response.content)

    def test_account_detail(self):

        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('accounts:detail'))

        # see that there is an image present (the usericon image)
        self.assertIn(b'usericon.svg', response.content)

class ProjectListPageTests(TestCase):
    """
    Test that user can see their list of projects
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

    def test_list_exists(self):

        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('projects:all'))
        # See project title
        self.assertIn(b'fake_title', response.content)
        # See how many members there are in the project
        self.assertIn(b'"Members">4', response.content)
        # See how many records there are in the project
        self.assertIn(b'"Records">10', response.content)
        # see that the user can go to the specific project
        self.assertIn(b'<a href="/projects/fake_title3/"', response.content)
        # see that the user can go to create a new project
        self.assertIn(b'<a href="/projects/new/"', response.content)


class ProjectMemberModelTests(TestCase):
    """
    Testing to see that the projectmember model is accurate
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


    def test_membercount(self):
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        projectmembers = models.ProjectMember.objects.filter(project=project).count()
        self.assertEqual(projectmembers, project.members.count())

    def test_permissions(self):
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        projectmembers = models.ProjectMember.objects.filter(project=project, is_owner=True).count()
        self.assertEqual(projectmembers, 0)

        projectmembers = models.ProjectMember.objects.filter(project=project, is_reader=True).count()
        self.assertEqual(projectmembers, 0)

        projectmembers = models.ProjectMember.objects.filter(project=project, is_editor=True).count()
        self.assertEqual(projectmembers, 3)

        from django.contrib.auth import get_user_model
        User = get_user_model()
        testuser =  User.objects.create_user('testuser', 'foo@example.com', 'pass')
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        pm = models.ProjectMember.objects.get_or_create(user=testuser, project=project, is_owner=True)

        projectmembers = models.ProjectMember.objects.filter(project=project, is_owner=True).count()
        self.assertEqual(projectmembers, 1)

    def test_model_cascade(self):
        from projects import models
        project = models.Project.objects.get(project_title="fake_title")
        projectmembers = models.ProjectMember.objects.filter(project=project).count()
        self.assertEqual(projectmembers, 3)
        project.delete()

        # testing to see that memberships are deleted when projects are
        projectmembers = models.ProjectMember.objects.all().count()
        self.assertEqual(projectmembers, 0)
