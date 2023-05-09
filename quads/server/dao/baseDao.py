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


class EntryExisting(Exception):
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
        query_columns = cls.create_query_columns(model=model, columns=columns)
        query = db.session.query(*query_columns).distinct(model.id)
        for expression in filters:
            try:
                column_name, op, value = expression
            except ValueError:
                raise Exception("Invalid filter: %s" % expression)
            if op not in FILTERING_OPERATORS:
                raise Exception("Invalid filter operation: %s" % op)
            attrs = column_name.split(".")
            if len(attrs) > 1:
                column_name = attrs[0]
                parent_column = MAP_MODEL[column_name]
                column = getattr(parent_column, attrs[1])
                query = query.filter(model.id == parent_column.host_id)
            else:
                column = getattr(model, column_name, None)
            if not column:
                raise Exception("Invalid filter column: %s" % column_name)
            else:
                try:
                    attr = (
                            list(
                                filter(
                                    lambda e: hasattr(column, e % FILTERING_OPERATORS[op]),
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
                query = query.filter(getattr(column, attr)(value))
        return query.all()

    @classmethod
    def create_query_columns(cls, model, columns):
        if not columns:
            return [model]

        cols = []
        for column in columns:
            attr = getattr(model, column, None)
            if not attr:
                raise Exception("Invalid column name %s" % column)
            cols.append(attr)
        return cols
