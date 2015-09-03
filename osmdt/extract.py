def _collate_data(collation, first_axis, second_axis):
    """
    """
    if first_axis not in collation:
        collation[first_axis] = {}
        collation[first_axis]["create"] = 0
        collation[first_axis]["modify"] = 0
        collation[first_axis]["delete"] = 0

    first = collation[first_axis]

    first[second_axis] = first[second_axis] + 1

    collation[first_axis] = first


def extract_changesets(objects):
    """
    """
    def add_changeset_info(collation, axis, item):
        """
        """
        if axis not in collation:
            collation[axis] = {}

        first = collation[axis]

        first["username"] = item["username"]
        first["uid"] = item["uid"]
        first["timestamp"] = item["timestamp"]

        collation[axis] = first

    changeset_collation = {}

    for node in objects.nodes.values():
        _collate_data(changeset_collation, node['changeset'], node['action'])
        add_changeset_info(changeset_collation, node['changeset'], node)
    for way in objects.ways.values():
        _collate_data(changeset_collation, way['changeset'], way['action'])
        add_changeset_info(changeset_collation, way['changeset'], way)
    for relation in objects.relations.values():
        _collate_data(changeset_collation, relation['changeset'], relation['action'])
        add_changeset_info(changeset_collation, relation['changeset'], relation)

    return changeset_collation


def extract_objects(objects):
    """
    """
    def add_object_info(collation, axis, item):
        """
        """
        if axis not in collation:
            collation[axis] = {}

        first = collation[axis]

        first["username"] = item["username"]
        first["uid"] = item["uid"]
        first["timestamp"] = item["timestamp"]
        first["changeset"] = item["changeset"]
        first["version"] = item["version"]
        first["tags"] = {}
        for key in item["tags"]:
            first["tags"][key] = item["tags"][key]

        collation[axis] = first

    object_collation = {}

    for node in objects.nodes.values():
        _collate_data(object_collation, 'n'+str(node['id']), node['action'])
        add_object_info(object_collation, 'n'+str(node['id']), node)
    for way in objects.ways.values():
        _collate_data(object_collation, 'w'+str(way['id']), way['action'])
        add_object_info(object_collation, 'w'+str(way['id']), way)
    for relation in objects.relations.values():
        _collate_data(object_collation, 'r'+str(relation['id']), relation['action'])
        add_object_info(object_collation, 'r'+str(relation['id']), relation)

    return object_collation


def extract_users(objects):
    """
    """
    def add_user_info(collation, axis, item):
        """
        """
        if axis not in collation:
            collation[axis] = {}
            collation[axis]["timestamps"] = []
            collation[axis]["changesets"] = []

        first = collation[axis]

        first["uid"] = item["uid"]
        if item["changeset"] not in first["changesets"]:
            first["changesets"].append(item["changeset"])
            first["timestamps"].append(item["timestamp"])
        _collate_data(first, "action", item["action"])

        collation[axis] = first

    user_collation = {}

    for node in objects.nodes.values():
        add_user_info(user_collation, node['username'], node)
    for way in objects.ways.values():
        add_user_info(user_collation, way['username'], way)
    for relation in objects.relations.values():
        add_user_info(user_collation, relation['username'], relation)

    return user_collation
