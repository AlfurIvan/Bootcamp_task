"""Module for testing the services.py module."""

from django.test import TestCase

from ..models import Profession, Skill, Topic
from ..serializers import ProfessionSerializer
from ..services import (nested_relations_when_create,
                        nested_relations_when_update,
                        update_by_serializer,
                        _update_skill_or_topic_obj)


class ServicesTestCase(TestCase):
    """Tests for the services module."""
    def test_fill_relations_during_creation(self):
        nested_data = [
            {"name": "Skill1", "description": "Description1"},
            {"name": "Skill2", "description": "Description2"},
        ]

        created_objects = nested_relations_when_create(nested_data, Skill)
        created_objects.sort(key=lambda obj: obj.name)

        self.assertIsInstance(created_objects, list)

        for obj in created_objects:
            self.assertIsInstance(obj, Skill)

        self.assertEqual(len(created_objects), len(nested_data))

        for obj, data in zip(created_objects, nested_data):
            for key, value in data.items():
                self.assertEqual(getattr(obj, key), value)

    def test_nested_relation_when_update(self):
        nested_data = [
            {
                "name": "Topic1",
                "description": "Description1",
                "pet_project_ideas": "IDEAS 1",
                "links": [
                    "https://refactoring.guru/design-patterns",
                    "https://sourcemaking.com/design_patterns",
                    "https://www.tutorialspoint.com/design_pattern/"
                ]
            },
            {
                "name": "Topic2",
                "description": "Description2",
                "pet_project_ideas": "IDEAS 2",
                "links": [
                    "https://www.djangoproject.com/",
                    "https://www.django-rest-framework.org/",
                    "https://channels.readthedocs.io/en/stable/"
                ]
            }
        ]

        returned_objs = nested_relations_when_update(nested_data, Topic)
        returned_objs.sort(key=lambda obj: obj.name)
        self.assertIsInstance(returned_objs, list)

        self.assertEqual(len(returned_objs), len(nested_data))

        for obj, data in zip(returned_objs, nested_data):
            for key, value in data.items():
                self.assertEqual(getattr(obj, key), value)

    def test_update_serialize_save_instance(self):
        profession = Profession.objects.create(
            uuid="28f07eef-7ba7-4427-a21f-f4393933b12e",
            name="Software Engineer",
            description="DO",
            average_salary=90000,
        )

        data = {
            "uuid": "28f07eef-7ba7-4427-a21f-f4393933b12e",
            "name": "Frontend Developer",
            "description": "description 1",
            "average_salary": 80000,
            "skills": []
        }

        updated_instance = update_by_serializer(ProfessionSerializer, profession, data)

        self.assertEqual(updated_instance.data['name'], "Frontend Developer")
        self.assertEqual(updated_instance.data['description'],
                         "description 1")
        self.assertEqual(updated_instance.data['average_salary'], 80000)

    def test_update_skill_obj(self):
        skill = Skill.objects.create(
            name="Python Programming",
            description="Skill in Python programming language."
        )

        data = {
            "name": "JavaScript Programming",
            "description": "Skill in JavaScript programming language."
        }

        updated_skill = _update_skill_or_topic_obj(skill, data)

        self.assertEqual(updated_skill.name, "JavaScript Programming")
        self.assertEqual(updated_skill.description, "Skill in JavaScript programming language.")

    def test_update_topic_obj(self):
        topic = Topic.objects.create(
            name="Web Development",
            description="Topic covering various aspects of web development.",
            pet_project_ideas="Build a personal website.",
            links="https://example.com"
        )

        data = {
            "name": "Mobile Development",
            "description": "Topic covering various aspects of mobile app development.",
            "pet_project_ideas": "Build a simple mobile app.",
            "links": "https://example.com/mobile"
        }

        updated_topic = _update_skill_or_topic_obj(topic, data)

        self.assertEqual(updated_topic.name, "Mobile Development")
        self.assertEqual(updated_topic.description, "Topic covering various aspects of mobile app development.")
        self.assertEqual(updated_topic.pet_project_ideas, "Build a simple mobile app.")
        self.assertEqual(updated_topic.links, "https://example.com/mobile")
