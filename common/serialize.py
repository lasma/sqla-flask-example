# -*- coding: utf-8 -*-
from common.utils import orm
from common.utils.dictionary import serializable


def get_as_dict(record, depth):
    """convert ORM record to Python dictionary"""
    #return {} if not record else record.get_as_dict(depth)
    return {} if not record else serializable_record(record, depth)

# TODO: make sure unicode is supported
def serializable_record(record, depth=1):
    """Generic method for dict conversion.

    @param record: the record to convert
    @param depth: depth until which any relationships should be exploded as subnodes in the main dictionary
    """

    if not record:
        return {}
    dictionary = orm.get_column_data_only(record)
    # dictionary = orm.extract_non_orm_props(dictionary)

    dictionary = serializable(dictionary)

    # Explode relationships into dictionaries and attach to the main dictionary (add as subnodes)
    if depth > 0:
        local_depth = depth
        while local_depth > 0:
            local_depth -= 1
            relationships = orm.get_relationships(record)
            for relationship in relationships:
                attribute_name = orm.get_relationship_name(relationship)
                attribute = getattr(record, attribute_name)
                if not attribute:
                    dictionary[attribute_name] = None
                else:
                    if isinstance(attribute, list):
                        attribute_dictionary = [attr.get_as_dict(depth=local_depth) for attr in attribute]
                    else:
                        attribute_dictionary = attribute.get_as_dict(depth=local_depth)
                    dictionary[attribute_name] = attribute_dictionary

    return dictionary

