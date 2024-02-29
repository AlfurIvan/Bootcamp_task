"""API endpoints for professions module."""
from rest_framework import generics, response

from . import models
from . import serializers
from .services import nested_relations_when_update, update_by_serializer


class ProfessionListCreateAPI(generics.ListCreateAPIView):
    """
    GET /professions/ - Retrieve all professions.
    POST /professions/ - Create a new profession
    """
    queryset = models.Profession.objects.all()
    serializer_class = serializers.ProfessionSerializer


class ProfessionRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /professions/{uuid}/ - Retrieve a Profession with given UUID
    PUT or PATCH /professions/{uuid}/ - Update a Profession with given UUID
    DELETE /professions/{uuid}/ - Delete a Profession with given UUID
    """
    queryset = models.Profession.objects.all()
    serializer_class = serializers.ProfessionSerializer

    def update(self, request, *args, **kwargs):
        """custom update method to hande updating nested Skill objects"""
        instance = models.Profession.objects.get(uuid=request.data.get('uuid'))
        skills_data = request.data.pop("skills")
        request.data["skills"] = []

        serializer = update_by_serializer(serializers.ProfessionSerializer, instance, data=request.data)

        if len(skills_data) != 0:
            list_of_relations_objects = nested_relations_when_update(skills_data, models.Skill)

            instance.skills.clear()
            instance.skills.set(list_of_relations_objects)

        return response.Response(serializer.data)


class SkillListCreateAPI(generics.ListCreateAPIView):
    """
    GET /skills/ - Retrieve all skills
    POST /skills/ - Create a new skill
    """
    queryset = models.Skill.objects.all()
    serializer_class = serializers.SkillSerializer


class SkillRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /skills/{uuid}/ - Retrieve a Skill with given UUID
    PUT or PATCH /skills/{uuid}/  - Update a Skill with given UUID
    DELETE /skills/{uuid}/   - Delete a Skill with given UUID
    """
    queryset = models.Skill.objects.all()
    serializer_class = serializers.SkillSerializer

    def update(self, request, *args, **kwargs):
        """custom update method to hande updating nested Topics objects"""
        instance = self.get_object()
        topics_data = request.data.pop("topics")
        request.data["topics"] = []

        serializer = update_by_serializer(serializers.SkillSerializer, instance, data=request.data)

        if len(topics_data) != 0:
            list_of_relations_objects = nested_relations_when_update(topics_data, models.Topic)
            instance.topics.clear()
            instance.topics.set(list_of_relations_objects)

        return response.Response(serializer.data)


class TopicListCreateAPI(generics.ListCreateAPIView):
    """
    GET /topics/   - List all topics
    POST /topics/   - Create a new topic
    """
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer


class TopicRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /topics/{uuid}/   - Retrieve a Topic with given UUID
    PUT or PATCH /topics/{uuid}  - Update a Topic with given UUID
    DELETE /topics/{uuid}   - Delete a Topic with given UUID
    """
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
