from .models import Topic


def nested_relation_when_create(nested_data, db_model) -> list:
    obj_list = []
    for skill_data in nested_data:
        obj, _ = db_model.objects.get_or_create(**skill_data)
        obj_list.append(obj)
    return obj_list


def nested_relation_when_update(nested_data, db_model) -> list:
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


def update_serialize_save_instance(serializer_class, instance, data):
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
