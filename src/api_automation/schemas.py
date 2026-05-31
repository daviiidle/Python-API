from __future__ import annotations

from typing import Any

Schema = dict[str, Any]

USER_SCHEMA: Schema = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "address": {"type": "object"},
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {"type": "object"},
    },
    "additionalProperties": True,
}

POST_SCHEMA: Schema = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "additionalProperties": True,
}

SCHEMAS: dict[str, Schema] = {
    "users_list": {
        "type": "array",
        "minItems": 1,
        "items": USER_SCHEMA,
    },
    "single_user": USER_SCHEMA,
    "posts_list": {
        "type": "array",
        "minItems": 1,
        "items": POST_SCHEMA,
    },
    "single_post": POST_SCHEMA,
    "created_post": {
        "type": "object",
        "required": ["userId", "id", "title", "body"],
        "properties": {
            "userId": {"type": "integer"},
            "id": {"type": "integer"},
            "title": {"type": "string", "minLength": 1},
            "body": {"type": "string", "minLength": 1},
        },
        "additionalProperties": True,
    },
    "empty_object": {
        "type": "object",
        "maxProperties": 0,
    },
}
