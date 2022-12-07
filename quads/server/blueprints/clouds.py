import json

from flask import Blueprint, jsonify, request, Response
from sqlalchemy import Boolean
from sqlalchemy.orm import RelationshipProperty

from quads.server.blueprints import check_access
from quads.server.dao.baseDao import OPERATORS, MAP_MODEL
from quads.server.dao.cloud import CloudDao
from quads.server.models import Cloud, db


cloud_bp = Blueprint("clouds", __name__)


@cloud_bp.route("/<cloud>/")
def get_cloud(cloud: str) -> Response:
    _cloud = CloudDao.get_cloud(cloud)
    return jsonify(_cloud.as_dict())


@cloud_bp.route("/")
def get_clouds() -> Response:
    # TODO: Add filter for child objects
    filter_tuples = []
    operator = "=="
    for k, value in request.args.items():
        fields = k.split(".")
        if len(fields) > 2:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Too many arguments: {fields}",
            }
            return Response(response=json.dumps(response), status=400)

        first_field = fields[0]
        field_name = fields[-1]
        if "__" in k:
            for op in OPERATORS.keys():
                if op in field_name:
                    field_name = field_name[: field_name.index(op)]
                    operator = OPERATORS[op]
                    break

        field = Cloud.__mapper__.attrs.get(first_field)
        if not field:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"{k} is not a valid field.",
            }
            return Response(response=json.dumps(response), status=400)
        if (
            type(field) != RelationshipProperty
            and type(field.columns[0].type) == Boolean
        ):
            value = value.lower() in ["true", "y", 1, "yes"]
        else:
            if first_field.lower() in MAP_MODEL.keys():
                if len(fields) > 1:
                    field_name = f"{first_field.lower()}.{field_name.lower()}"
        filter_tuples.append(
            (
                field_name,
                operator,
                value,
            )
        )
    if filter_tuples:
        _clouds = CloudDao.create_query_select(Cloud, filters=filter_tuples)
    else:
        _clouds = CloudDao.get_clouds()

    return jsonify([_cloud.as_dict() for _cloud in _clouds])


@cloud_bp.route("/", methods=["POST"])
@check_access("admin")
def create_cloud() -> Response:
    data = request.get_json()
    cloud_name = data.get("name")
    if not cloud_name:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: name",
        }
        return Response(response=json.dumps(response), status=400)

    _cloud = CloudDao.get_cloud(cloud_name)
    if _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Cloud {cloud_name} already exists",
        }
        return Response(response=json.dumps(response), status=400)

    _cloud_obj = Cloud(name=cloud_name)
    db.session.add(_cloud_obj)
    db.session.commit()
    return jsonify(_cloud_obj.as_dict())


@cloud_bp.route("/", methods=["DELETE"])
@check_access("admin")
def delete_cloud() -> Response:
    data = request.get_json()
    cloud_name = data.get("name")

    if not cloud_name:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: name",
        }
        return Response(response=json.dumps(response), status=400)

    _cloud = CloudDao.get_cloud(cloud_name)
    if not _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Cloud {cloud_name} not found",
        }
        return Response(response=json.dumps(response), status=400)
    db.session.delete(_cloud)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": f"Cloud {cloud_name} deleted",
        }
    )
