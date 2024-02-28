from django.urls import path
from . import apis

urlpatterns = [
    path('professions/', apis.ProfessionListCreateAPI.as_view()),
    path('professions/<uuid:pk>/', apis.ProfessionRetrieveUpdateDestroyAPI.as_view()),
    path('skills/', apis.SkillListCreateAPI.as_view()),
    path('skills/<uuid:pk>/', apis.SkillRetrieveUpdateDestroyAPI.as_view()),
    path('topics/', apis.TopicListCreateAPI.as_view()),
    path('topics/<uuid:pk>/', apis.TopicRetrieveUpdateDestroyAPI.as_view())
]
