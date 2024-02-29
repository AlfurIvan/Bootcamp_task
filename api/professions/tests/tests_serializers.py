"""Module containing tests for serializers."""
from django.test import TestCase

from ..models import Profession, Skill, Topic
from ..serializers import ProfessionSerializer, SkillSerializer, TopicSerializer


class ProfessionSerializerTest(TestCase):
    """Tests for Profession serializer."""
    def test_profession_create(self):
        serializer_data = {
            'name': 'Test Profession',
            'description': 'Test Description',
            'average_salary': 50000,
            'skills': []
        }

        serializer = ProfessionSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertIsInstance(instance, Profession)
        self.assertEqual(instance.name, 'Test Profession')

    def test_profession_update(self):
        profession = Profession.objects.create(name='Initial Name',
                                               description='Initial Description',
                                               average_salary=40000)
        serializer_data = {'uuid': profession.uuid,
                           'name': 'Updated Name',
                           'description': 'Updated Description',
                           'average_salary': 45000, 'skills': []}

        serializer = ProfessionSerializer(instance=profession, data=serializer_data, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, 'Updated Name')


class SkillSerializerTest(TestCase):
    """Tests for Skill serializer"""
    @classmethod
    def setUpTestData(cls):
        cls.topic = Topic.objects.create(name='Test Topic', description='Test Description')

    def test_skill_create(self):
        serializer_data = {
            'name': 'Test Skill',
            'description': 'Test Description',
            'topics': [],
        }

        serializer = SkillSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertIsInstance(instance, Skill)
        self.assertEqual(instance.name, 'Test Skill')

    def test_skill_update(self):
        skill = Skill.objects.create(name='Initial Name', description='Initial Description')
        serializer_data = {'name': 'Updated Name', 'description': 'Updated Description'}

        serializer = SkillSerializer(instance=skill, data=serializer_data, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, 'Updated Name')


class TopicSerializerTest(TestCase):
    """Tests for TopicSerializer"""
    @classmethod
    def setUpTestData(cls):
        skill = Skill.objects.create(name="Test Skill", description="Test Skill Description")
        cls.topic_data = {
            'name': 'Test Topic',
            'description': 'Test Description',
            'pet_project_ideas': 'Test Project Ideas',
            'links': 'Link1, Link2, Link3',
            'skill': skill.uuid
        }

    def test_topic_serializer(self):
        skill = Skill.objects.get(name="Test Skill")
        serializer = TopicSerializer(data=self.topic_data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, 'Test Topic')
        self.assertEqual(instance.description, 'Test Description')
        self.assertEqual(instance.pet_project_ideas, 'Test Project Ideas')
        self.assertEqual(instance.links, 'Link1, Link2, Link3')
        self.assertEqual(instance.skill, skill)
