# -*- coding: utf-8 -*-

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute, QueryableAttribute
from sqlalchemy.sql.expression import BinaryExpression
from model.base import Base

def is_orm_class(object):
    """
    Check if specified object is ORM class

    @param object:  any python object

    @return: boolean

    """
    return isinstance(object, DeclarativeMeta) or isinstance(object, Base)


def get_relationships(any_orm_class):
    """Get a list of SqlAlchemy's relationships declared on the input ORM class.

    :param any_orm_class: any ORM class
    :return a list of relationships declared on the input class
    """
    i = inspect(any_orm_class)
    relationships = i.mapper.relationships
    return relationships


def get_sqlalchemy_type_for_attribute(attribute):
    """Given a SQLAlchemy attribute, get the SQLAlchemy type for it.

    For example, Integer, Float, Boolean, Geometry)
    """
    attr_type = None
    if isinstance(attribute, BinaryExpression):
        attr_type = attribute.type
    elif isinstance(attribute, InstrumentedAttribute):
        attr_type = attribute.property.columns[0].type
    elif isinstance(attribute, QueryableAttribute):
        attr_type = attribute.property.expression.type
    else:
        raise NotImplementedError
    return attr_type


def get_relationship_name(any_orm_relationship):
    """Get string name for the input ORM relationship object"""
    return any_orm_relationship.strategy.key


def get_class_from_relationship(any_orm_relationship):
    """Return the class (DeclarativeMeta child) mapped to the provided relationship"""
    relationship_class = any_orm_relationship.mapper.entity
    return relationship_class


def alias_primary_join(relationship, model):
    """
    Alias the primary join clause of a relationship in an ORM model.
    This is needed as when alias is called on the orm model to create an alias,
    the primary join expression does not get mutated to use the new aliased class names.
    """
    primary_join = relationship.primaryjoin

    right_table = primary_join.right.table
    left_table = primary_join.left.table
    relationship_table = relationship.table

    # We do not necessarily know where the primary model and the relationship model lie in the expression,
    # it could be either left or right.
    if relationship_table == left_table:
        primary_join.left = model.id.expression
    elif relationship_table == right_table:
        primary_join.right = model.id.expression

    return primary_join


def get_synonyms(orm_class):
    """
    Get a list of synonyms for columns in the given ORM class

    @param orm_class    Some ORM class

    @return {list}      A list of synonyms being used in the provided ORM class.
    """
    keys = list()
    if is_orm_class(orm_class) is True:
        i = inspect(orm_class)
        keys = i.synonyms._data.keys()
    return keys


def get_column_names(orm_class):
    """Get a list of column names for the given ORM table class

    @param orm_class    Some ORM class, for example, StatusType

    @return {list}      List of column names for the given ORM table class, e.g.
    ['order_id', 'requestor_id', 'order_type_id', 'assigned_cxam_id', 'deputy_cxam_id']
    """

    keys = list()

    if is_orm_class(orm_class) is True:
        # This would give column names prefixed with table name:
        # orm_class.order.__table__.columns

        # Get a list of column names without table name prefix
        keys = orm_class.__table__.columns._data.keys()

    return keys


def get_columns_and_types(orm_class):
    """
    Get a dictionary of column names and column data types for the given ORM table class

    @param orm_class    Some ORM class, for example, StatusType

    @return {dict} for example
    `{
        'order_id': Integer(),
        'order_type_id': Integer(),
        'assigned_cxam_id': Integer(),
        'requestor_id': Integer(),
        'deputy_cxam_id': Integer()
    }`
    """

    columns = dict()

    if is_orm_class(orm_class) is True:

        cols = orm_class.__table__.columns
        for c in cols:
            columns[c.name] = c.type

    return columns


def get_column_data_only(orm_record):
    """
    Parse ORM record and return only data that is part of the database record.

    Class specific properties will be parsed out.

    @param orm_record:              SqlAlchemy's ORM record from any table
    @return {dict}                  ORM record as python dictionary only having nodes that represent database
                                    column and values for this particular ORM record
    """
    new_data = dict()

    if orm_record is not None:
        columns = get_column_names(orm_record)
        for column in columns:
            try:
                new_data[column] = getattr(orm_record, column)
            except:
                pass

    return new_data


def get_class_by_tablename(tablename):
    """Return ORM class reference mapped to table.

    :param tablename:   String with name of table.
    :return:            Class reference or None.
    """
    # for c in OmsDeclarativeBase._decl_class_registry.values():
    # if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
    # return c

    try:
        any_orm_class = OmsDeclarativeBase._decl_class_registry[tablename]
    except Exception as e:
        print e
        any_orm_class = None

    return any_orm_class

