from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Profession, Skill, Topic
from ..serializers import ProfessionSerializer


class ProfessionListCreateAPITest(APITestCase):

    def test_get_professions(self):
        profession1 = Profession.objects.create(name='Test Profession 1', description='Test Description 1')
        profession2 = Profession.objects.create(name='Test Profession 2', description='Test Description 2')

        response = self.client.get('http://0.0.0.0:8000/professions/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), Profession.objects.count())

        expected_data = ProfessionSerializer([profession1, profession2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_create_profession(self):
        profession_data = {
            'name': 'New Test Profession',
            'description': 'New Test Description',
            'average_salary': 10000,
            'skills': []
        }

        response = self.client.post('http://0.0.0.0:8000/professions/', profession_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Profession.objects.filter(name='New Test Profession').exists())

        self.assertEqual(response.data['name'], 'New Test Profession')
        self.assertEqual(response.data['description'], 'New Test Description')


class SkillListCreateAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.skill1 = Skill.objects.create(name='Test Skill 1', description='Test Description 1')
        cls.skill2 = Skill.objects.create(name='Test Skill 2', description='Test Description 2')

    def test_get_skills(self):
        url = 'http://0.0.0.0:8000/skills/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), Skill.objects.count())

        self.assertEqual(response.data[0]['name'], 'Test Skill 1')
        self.assertEqual(response.data[0]['description'], 'Test Description 1')

    def test_create_skill(self):
        url = 'http://0.0.0.0:8000/skills/'

        new_skill_data = {'name': 'New Skill', 'description': 'New Description', 'topics': []}

        response = self.client.post(url, new_skill_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Skill.objects.filter(name='New Skill').exists())

        self.assertEqual(response.data['name'], 'New Skill')
        self.assertEqual(response.data['description'], 'New Description')


class TopicListCreateAPITest(APITestCase):

    def setUp(self):
        self.url = 'http://0.0.0.0:8000/topics/'
        self.topic_data = {
            "name": "Django",
            "description": "blah",
            "pet_project_ideas": "blah blah",
            "links": [
                "https://www.djangoproject.com/",
                "https://realpython.com/tutorials/django/",
                "https://www.djangoproject.com/start/"
            ]
        }

    def test_get_topics(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Topic.objects.count())

        for topic in response.data:
            self.assertIn('name', topic)
            self.assertIn('description', topic)
            self.assertIn('pet_project_ideas', topic)
            self.assertIn('links', topic)

    def test_create_topic(self):
        response = self.client.post(self.url, self.topic_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Topic.objects.filter(name='Django').exists())

        for key, value in self.topic_data.items():
            self.assertEqual(response.data[key], value)

    def test_create_topic_invalid_data(self):
        invalid_topic_data = {
            "name": "",
            "description": "A high-level Python web framework",
            "pet_project_ideas": "1. Build a blog application with user authentication and CRUD operations.",
            "links": [
                "https://www.djangoproject.com/"
            ]
        }
        response = self.client.post(self.url, invalid_topic_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(Topic.objects.filter(name='').exists())


class TopicRetrieveUpdateDestroyAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.topic = Topic.objects.create(
            name="Django",
            description="foobarfoobar",
            pet_project_ideas="foobarfoobar foobarfoobar",
            links=[
                "https://www.djangoproject.com/",
                "https://realpython.com/tutorials/django/",
                "https://www.djangoproject.com/start/"
            ]
        )

    def test_retrieve_topic(self):
        url = f'http://0.0.0.0:8000/topics/{self.topic.uuid}/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Перевірте, чи повертається правильна структура даних
        self.assertEqual(response.data['name'], 'Django')
        self.assertEqual(response.data['description'], 'foobarfoobar')

    def test_update_topic(self):
        url = f'http://0.0.0.0:8000/topics/{self.topic.uuid}/'

        updated_data = {
            "name": "Updated Django",
            "description": "An updated description."

        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, 'Updated Django')
        self.assertEqual(self.topic.description, 'An updated description.')

    def test_delete_topic(self):
        url = f'http://0.0.0.0:8000/topics/{self.topic.uuid}/'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ObjectDoesNotExist):
            Topic.objects.get(pk=self.topic.pk)