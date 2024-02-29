"""Serializers for the Professions app."""
from rest_framework import serializers

from .models import Profession, Skill, Topic
from .services import nested_relations_when_create


class SplitLinksField(serializers.Field):
    """Custom slicer-joiner for 'links' field."""
    def to_representation(self, obj):
        """Split the links by ', '"""
        if obj:
            return obj.split(', ')
        return []

    def to_internal_value(self, data):
        """Join the links back into a single string separated by ', '"""
        if isinstance(data, list):
            return ', '.join(data)
        return data


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for Topics model"""
    links = SplitLinksField()

    class Meta:
        model = Topic
        fields = ['uuid', 'name', 'description', 'pet_project_ideas', 'links', 'skill']


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model"""
    topics = TopicSerializer(many=True, allow_null=True)

    class Meta:
        model = Skill
        fields = ['uuid', 'name', 'description', 'topics']

    def create(self, validated_data):
        """custom creating handler to resolve problems with nested 'topics' fields """
        topics_data = validated_data.pop("topics")

        instance = Skill.objects.create(**validated_data)
        if len(topics_data):
            topics_set = nested_relations_when_create(topics_data, Topic)
            instance.topics.set(topics_set)

        return instance

    def update(self, instance, validated_data):
        """custom updating handler to resolve problems with nested 'topics' fields """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance


class ProfessionSerializer(serializers.ModelSerializer):
    """Serializer for Profession model"""
    uuid = serializers.UUIDField(read_only=True)
    skills = SkillSerializer(many=True, allow_null=True)

    class Meta:
        model = Profession
        fields = ['uuid', 'name', 'description', 'average_salary', 'skills', 'last_updated']

    def create(self, validated_data):
        """custom creating handler to resolve problems with nested 'skill' fields """
        skills_data = validated_data.pop("skills")

        instance = Profession.objects.create(**validated_data)

        if len(skills_data):
            skills_set = nested_relations_when_create(skills_data, Topic)
            instance.skills.set(skills_set)

        return instance

    def update(self, instance, validated_data):
        """custom creating handler to resolve problems with nested 'skills' fields """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.average_salary = validated_data.get('average_salary', instance.average_salary)

        instance.save()
        return instance
