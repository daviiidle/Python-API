from __future__ import annotations

import json
from typing import Any

from behave import given, then, when
from jsonschema import validate

from src.api_automation.schemas import SCHEMAS


def _response_json(context: Any) -> Any:
    response = context.response
    assert response is not None, "No response is available. Send a request first."
    if not response.text:
        return {}
    return response.json()


def _coerce_value(value: str) -> Any:
    normalized = value.strip()
    if normalized.lower() == "true":
        return True
    if normalized.lower() == "false":
        return False
    if normalized.lower() == "null":
        return None
    try:
        return int(normalized)
    except ValueError:
        return normalized


def _get_field(document: Any, path: str) -> Any:
    value = document
    for part in path.split("."):
        if isinstance(value, list):
            value = value[int(part)]
        else:
            value = value[part]
    return value


@given('the API endpoint is "{endpoint}"')
def set_endpoint(context: Any, endpoint: str) -> None:
    context.endpoint = endpoint


@given("the query parameters are")
def set_query_parameters(context: Any) -> None:
    context.query_params = {
        row["key"]: _coerce_value(row["value"])
        for row in context.table
    }


@given("I have a dynamic post payload")
def set_dynamic_post_payload(context: Any) -> None:
    context.request_payload = {
        "title": context.faker.sentence(nb_words=6).rstrip("."),
        "body": context.faker.paragraph(nb_sentences=3),
        "userId": context.faker.random_int(min=1, max=10),
    }


@given("the request payload is")
def set_request_payload(context: Any) -> None:
    context.request_payload = {
        row["key"]: _coerce_value(row["value"])
        for row in context.table
    }


@when("I send a GET request")
def send_get_request(context: Any) -> None:
    context.response = context.api.request(
        "GET",
        context.endpoint,
        params=context.query_params,
    )


@when("I send a POST request")
def send_post_request(context: Any) -> None:
    context.response = context.api.request(
        "POST",
        context.endpoint,
        json=context.request_payload,
    )


@when("I send a PUT request")
def send_put_request(context: Any) -> None:
    context.response = context.api.request(
        "PUT",
        context.endpoint,
        json=context.request_payload,
    )


@when("I send a DELETE request")
def send_delete_request(context: Any) -> None:
    context.response = context.api.request("DELETE", context.endpoint)


@then("the response status code should be {expected_status:d}")
def validate_status_code(context: Any, expected_status: int) -> None:
    actual_status = context.response.status_code
    assert actual_status == expected_status, (
        f"Expected status code {expected_status}, got {actual_status}. "
        f"Response body: {context.response.text}"
    )


@then('the response field "{field_path}" should equal "{expected_value}"')
def validate_field_equals_string(context: Any, field_path: str, expected_value: str) -> None:
    actual = _get_field(_response_json(context), field_path)
    assert actual == expected_value, (
        f'Expected "{field_path}" to equal "{expected_value}", got {actual!r}'
    )


@then('the response field "{field_path}" should equal {expected_value:d}')
def validate_field_equals_int(context: Any, field_path: str, expected_value: int) -> None:
    actual = _get_field(_response_json(context), field_path)
    assert actual == expected_value, (
        f'Expected "{field_path}" to equal {expected_value}, got {actual!r}'
    )


@then('the response field "{field_path}" should be a non-empty list')
def validate_field_is_non_empty_list(context: Any, field_path: str) -> None:
    actual = _get_field(_response_json(context), field_path)
    assert isinstance(actual, list), (
        f'Expected "{field_path}" to be a list, got {type(actual).__name__}'
    )
    assert actual, f'Expected "{field_path}" to be non-empty'


@then("the response body should be a non-empty list")
def validate_response_body_is_non_empty_list(context: Any) -> None:
    response_body = _response_json(context)
    assert isinstance(response_body, list), (
        f"Expected response body to be a list, got {type(response_body).__name__}"
    )
    assert response_body, "Expected response body to be non-empty"


@then("the response should include the request payload")
def validate_response_includes_request_payload(context: Any) -> None:
    response_body = _response_json(context)
    for key, expected_value in context.request_payload.items():
        actual_value = response_body.get(key)
        assert actual_value == expected_value, (
            f"Expected response field {key!r} to equal {expected_value!r}, got {actual_value!r}. "
            f"Full response: {json.dumps(response_body, indent=2)}"
        )


@then('the response should match the "{schema_name}" schema')
def validate_response_schema(context: Any, schema_name: str) -> None:
    schema = SCHEMAS.get(schema_name)
    assert schema is not None, (
        f"Unknown schema: {schema_name}. Available schemas: {sorted(SCHEMAS)}"
    )
    validate(instance=_response_json(context), schema=schema)
