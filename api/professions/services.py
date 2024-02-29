"""
Module for various functions which are just logic
They are doing some stuff
"""

from .models import Topic


def nested_relations_when_create(nested_data, db_model) -> list:
    """
    Method to separately collect(or create new) objects from :param nested_data: ,
    while CREATING something
    :param nested_data: list of JSONs
    :param db_model: db model class
    :return: list of instances of :param db_model:
    """
    obj_list = []
    for item_data in nested_data:
        obj, _ = db_model.objects.get_or_create(**item_data)
        obj_list.append(obj)
    return obj_list


def nested_relations_when_update(nested_data, db_model) -> list:
    """
    Method to separately collect(or create new) objects from :param nested_data: ,
    while UPDATING something
    :param nested_data: list of JSONs
    :param db_model: db model class
    :return: list of instances of :param db_model:
    """
    obj_list = []
    for item_data in nested_data:

        try:
            name = item_data.get("name")
            obj = db_model.objects.get(name=name)
            obj = _update_skill_or_topic_obj(obj, item_data)
        except db_model.DoesNotExist:
            obj = db_model.objects.create(**item_data)
        obj.save()
        obj_list.append(obj)
    return obj_list


def update_by_serializer(serializer_class, instance, data):
    """
    Method (to shut PyCharm) to update the instance using it`s serializer
    :param serializer_class: serializer_class for :param instance:
    :param instance: instance to be updated, validated and saved
    :param data: new data to update :param instance:
    :return: updated serialized instance
    """
    serial_data = serializer_class(instance, data=data, partial=True)
    serial_data.is_valid(raise_exception=True)
    serial_data.save()
    return serial_data


def _update_skill_or_topic_obj(obj, data):
    """update fields of Skill or Topic models"""
    obj.name = data.get("name", obj.name)
    obj.description = data.get("description", obj.description)
    if isinstance(obj, Topic):
        obj.pet_project_ideas = data.get("pet_project_ideas", obj.pet_project_ideas)
        obj.links = data.get("links", obj.links)
    obj.save()
    return obj
