"""Database models for Professions app."""
import uuid

from django.db import models


class Profession(models.Model):
    """Profession entity model"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="profession name")
    description = models.TextField(verbose_name="profession description")
    average_salary = models.IntegerField(null=True)
    last_updated = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField('Skill', related_name='professions', blank=True)

    def __str__(self):
        return str(self.name)


class Skill(models.Model):
    """Skill entity model"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="skill name")
    description = models.TextField(verbose_name="skill description")

    def __str__(self):
        return str(self.name)


class Topic(models.Model):
    """Topic entity model"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="topic name")
    description = models.TextField(verbose_name="topic description")
    pet_project_ideas = models.TextField(verbose_name="pet project ideas")
    links = models.TextField(max_length=2047, verbose_name="books/courses links")
    skill = models.ForeignKey(
        'Skill',
        on_delete=models.SET_NULL,
        related_name='topics',
        related_query_name='topic',
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.name)
