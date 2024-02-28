from .models import Topic


def fill_relations_during_creation(nested_data, db_model) -> set:
    nested_obj_list = []
    for skill_data in nested_data:
        obj, _ = db_model.objects.get_or_create(**skill_data)
        nested_obj_list.append(obj)
    return set(nested_obj_list)


def nested_relation_updater(nested_field_data, db_model):
    obj_list = []
    for item_data in nested_field_data:

        try:
            name = item_data.get("name")
            obj = db_model.objects.get(name=name)
            obj = update_unknown_obj(obj, item_data)
        except db_model.DoesNotExist:
            obj = db_model.objects.create(**item_data)
        obj.save()
        obj_list.append(obj)
    return obj_list


def update_serialize_save_instance(serializer_class, instance, data):
    serializer = serializer_class(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer


def update_unknown_obj(obj, data):
    obj.name = data.get("name", obj.name)
    obj.description = data.get("description", obj.description)
    if isinstance(obj, Topic):
        obj.pet_project_ideas = data.get("pet_project_ideas", obj.pet_project_ideas)
        obj.links = data.get("links", obj.links)
    obj.save()
    return obj
