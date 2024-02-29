from django.test import TestCase

from ..models import Profession, Skill, Topic


class ProfessionModelTest(TestCase):

    @classmethod
    def setUp(cls):
        Skill.objects.create(name="Test Skill", description="Test Skill Description")
        Profession.objects.create(
            name="Test Profession",
            description="Test Profession Description",
            average_salary=50000)

    def test_profession_creation(self):
        profession = Profession.objects.get(name="Test Profession")
        self.assertEqual(profession.description, "Test Profession Description")
        self.assertEqual(profession.average_salary, 50000)
        self.assertIsNotNone(profession.last_updated)

    def test_profession_skills(self):
        profession = Profession.objects.get(name="Test Profession")
        skill = Skill.objects.get(name="Test Skill")
        profession.skills.add(skill)
        self.assertIn(skill, profession.skills.all())

    def test_skill_str(self):
        profession = Profession.objects.get(description='Test Profession Description')
        self.assertEqual(str(profession), "Test Profession")


class SkillModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Skill.objects.create(name="Test Skill", description="Test Skill Description")

    def test_skill_creation(self):
        skill = Skill.objects.get(name="Test Skill")
        self.assertEqual(skill.description, "Test Skill Description")

    def test_skill_str(self):
        skill = Skill.objects.get(description='Test Skill Description')
        self.assertEqual(str(skill), "Test Skill")


class TopicModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        skill = Skill.objects.create(name="Test Skill", description="Test Skill Description")
        Topic.objects.create(name="Test Topic",
                             description="Test Topic Description",
                             pet_project_ideas="Test Project Ideas",
                             links="Test Links", skill=skill)

    def test_topic_creation(self):
        topic = Topic.objects.get(name="Test Topic")
        self.assertEqual(topic.description, "Test Topic Description")
        self.assertEqual(topic.pet_project_ideas, "Test Project Ideas")
        self.assertEqual(topic.links, "Test Links")
        self.assertEqual(topic.skill.name, "Test Skill")

    def test_topic_str(self):
        topic = Topic.objects.get(name="Test Topic")
        self.assertEqual(str(topic), "Test Topic")

