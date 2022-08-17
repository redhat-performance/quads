from sqlalchemy import and_, or_

from quads.server.models import db, Interface, Disk, Memory, Processor
from quads.server import models
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

FILTERING_OPERATORS = {
    "==": "eq",
    "!=": "ne",
    ">": "gt",
    "<": "lt",
    ">=": "ge",
    "<=": "le",
    "like": "like",
    "ilike": "ilike",
    "in": "in",
}
OPERATORS = {
    "__ne": "!=",
    "__lt": "<",
    "__lte": "<=",
    "__gt": ">",
    "__gte": ">=",
    "__like": "like",
    "__ilike": "ilike",
    "__in": "in",
}
MAP_MODEL = {
    "interfaces": Interface,
    "disks": Disk,
    "memory": Memory,
    "processors": Processor,
}


class EntryNotFound(Exception):
    pass


class BaseDao:
    @staticmethod
    def safe_commit() -> bool:
        """
        Safely attempt to commit changes to MySQL.  Rollback in case of a failure.
        :return: True if the commit was successful, False if a rollback occurred.
        """
        try:
            db.session.commit()
            current_app.logger.info("SQL Safely Committed")
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            current_app.logger.error("SQL Commit Failed!  Rolling back...")
            current_app.logger.error(error.args)
            return False

    @classmethod
    def create_query_select(cls, model, filters=None, columns=None):
        query_filter = cls.create_query_filter(model=model, filters=filters)
        query_columns = cls.create_query_columns(model=model, columns=columns)
        return db.session.query(*query_columns).filter(*query_filter).all()

    @classmethod
    def create_query_filter(cls, model, filters):
        """
        return sqlalchemy filter list
        Args:
            model:sqlalchemy  model (classe das tabelas)
            filters: filter dict
                     ex:
                        filters = {
                            'or_1':{
                                'and_1':[('id', '>', 5),('id', '!=', 3)],
                                'and_2':[('fase', '==', 'arquivado')]
                            },
                            'and':[('test', '==', 'test')]
                        }
        Returns:
            filt: sqlalchemy filter list
        """
        if not filters:
            return []

        filt = []
        for condition in filters:
            if type(filters[condition]) == dict:
                if "and" in condition:
                    filt.append(
                        and_(*cls.create_query_filter(model, filters[condition]))
                    )
                elif "or" in condition:
                    filt.append(
                        or_(*cls.create_query_filter(model, filters[condition]))
                    )
                else:
                    raise Exception("Invalid filter condition: %s" % condition)
                continue
            filt_aux = []
            for t_filter in filters[condition]:
                try:
                    column_name, op, value = t_filter
                except ValueError:
                    raise Exception("Invalid filter: %s" % t_filter)
                if not op in FILTERING_OPERATORS:
                    raise Exception("Invalid filter operation: %s" % op)
                attrs = column_name.split(".")
                if len(attrs) > 1:
                    column_name = attrs[0]
                    parent_column = MAP_MODEL[column_name]
                    column = getattr(parent_column, attrs[1])
                else:
                    column = getattr(model, column_name, None)
                if not column:
                    raise Exception("Invalid filter column: %s" % column_name)
                if FILTERING_OPERATORS[op] == "in":
                    filt.append(column.in_(value))
                else:
                    try:
                        attr = (
                            list(
                                filter(
                                    lambda e: hasattr(
                                        column, e % FILTERING_OPERATORS[op]
                                    ),
                                    ["%s", "%s_", "__%s__"],
                                )
                            )[0]
                            % FILTERING_OPERATORS[op]
                        )
                    except IndexError:
                        raise Exception(
                            "Invalid filter operator: %s" % FILTERING_OPERATORS[op]
                        )
                    if value == "null":
                        value = None
                    filt_aux.append(getattr(column, attr)(value))
            if "and" in condition:
                filt.append(and_(*filt_aux))
            elif "or" in condition:
                filt.append(or_(*filt_aux))
            else:
                raise Exception("Invalid filter condition: %s" % condition)
        import ipdb

        ipdb.set_trace()
        return filt

    @classmethod
    def create_query_columns(cls, model, columns):
        """
        Return a list of attributes (columns) from the class model
        Args:
            model: sqlalchemy model
            columns: string list
                     ex: ['id', 'cnj']
        Returns:
            cols: list of attributes from the class model
        """
        if not columns:
            return [model]

        cols = []
        for column in columns:
            attr = getattr(model, column, None)
            if not attr:
                raise Exception("Invalid column name %s" % column)
            cols.append(attr)
        return cols
