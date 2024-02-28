from rest_framework import generics, response

from . import models
from . import serializers
from .services import nested_relation_updater, update_serialize_save_instance


class ProfessionListCreateAPI(generics.ListCreateAPIView):
    queryset = models.Profession.objects.all()
    serializer_class = serializers.ProfessionSerializer


class ProfessionRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Profession.objects.all()
    serializer_class = serializers.ProfessionSerializer

    def update(self, request, *args, **kwargs):
        instance = models.Profession.objects.get(uuid=request.data.get('uuid'))
        skills_data = request.data.pop("skills")
        request.data["skills"] = []

        serializer = update_serialize_save_instance(serializers.ProfessionSerializer, instance, data=request.data)

        if len(skills_data) != 0:
            list_of_relations_objects = nested_relation_updater(skills_data, models.Skill)

            instance.skills.clear()
            instance.skills.set(list_of_relations_objects)

        return response.Response(serializer.data)


class SkillListCreateAPI(generics.ListCreateAPIView):
    queryset = models.Skill.objects.all()
    serializer_class = serializers.SkillSerializer


class SkillRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Skill.objects.all()
    serializer_class = serializers.SkillSerializer

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        topics_data = request.data.pop("topics")
        request.data["topics"] = []

        serializer = update_serialize_save_instance(serializers.SkillSerializer, instance, data=request.data)

        if len(topics_data) != 0:
            list_of_relations_objects = nested_relation_updater(topics_data, models.Topic)
            instance.topics.clear()
            instance.topics.set(list_of_relations_objects)

        return response.Response(serializer.data)


class TopicListCreateAPI(generics.ListCreateAPIView):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer


class TopicRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
