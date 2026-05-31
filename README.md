# API Automation Portfolio - Python Behave Requests

## Overview

This repository is a production-style API automation framework for a QA Automation Engineer portfolio. It uses Behave BDD feature files, reusable Python step definitions, Requests-based API execution, environment-based configuration, Faker-powered dynamic data, JSON schema validation, structured logging, and GitHub Actions CI.

The target API is [JSONPlaceholder](https://jsonplaceholder.typicode.com), a stable public demo API. The framework is designed so the base URL can be replaced with another API through `.env` without changing test code.

## Tech Stack

- Python 3.11
- Behave for BDD scenarios
- Requests for HTTP API calls
- Faker for dynamic request data
- jsonschema for contract validation
- python-dotenv for environment configuration
- Ruff for linting
- Mypy for type checking
- GitHub Actions for CI

## Folder Structure

```text
.
├── .github/workflows/api-tests.yml
├── features/
│   ├── environment.py
│   ├── posts.feature
│   ├── users.feature
│   └── steps/
│       └── api_steps.py
├── src/
│   └── api_automation/
│       ├── __init__.py
│       ├── client.py
│       ├── config.py
│       ├── logging_config.py
│       └── schemas.py
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

## How To Run Locally

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a local environment file:

```bash
cp .env.example .env
```

4. Run linting, type checks, and API tests:

```bash
ruff check .
mypy
behave --junit --junit-directory reports/junit -f json.pretty -o reports/behave-report.json -f pretty
```

Reports are written to the `reports/` directory.

## How CI/CD Works

GitHub Actions runs on every push, pull request, and manual workflow dispatch.

The workflow:

- Checks out the repository.
- Sets up Python 3.11.
- Installs dependencies from `requirements.txt`.
- Runs Ruff linting.
- Runs Mypy type checking.
- Executes Behave API tests.
- Uploads generated Behave JSON and JUnit reports as CI artifacts.

## Example Scenarios

```gherkin
Scenario: Retrieve a paginated list of users
  Given the API endpoint is "/users"
  And the query parameters are:
    | key   | value |
    | _page | 1     |
    | _limit| 3     |
  When I send a GET request
  Then the response status code should be 200
  And the response body should be a non-empty list
  And the response field "0.id" should equal 1
  And the response should match the "users_list" schema
```

```gherkin
Scenario: Create a post using dynamic test data
  Given the API endpoint is "/posts"
  And I have a dynamic post payload
  When I send a POST request
  Then the response status code should be 201
  And the response should include the request payload
  And the response should match the "created_post" schema
```

## What This Project Demonstrates

- BDD API test design using reusable Behave steps.
- Clean separation between framework code, feature files, and test data generation.
- Positive and negative API scenario coverage.
- Status code, response body, and JSON schema validation.
- Environment-driven configuration through `.env`.
- Requests session reuse and timeout handling.
- Structured logging for local and CI troubleshooting.
- CI-ready quality gates with linting, type checking, test execution, and report artifacts.

## Notes

JSONPlaceholder is a demo API. POST, PUT, PATCH, and DELETE requests return realistic responses, but data is not permanently persisted.
