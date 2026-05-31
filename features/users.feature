Feature: Users API
  As a QA Automation Engineer
  I want to validate user endpoints
  So that API consumers can rely on response status, body, and contract behavior

  Scenario: Retrieve a paginated list of users
    Given the API endpoint is "/users"
    And the query parameters are
      | key    | value |
      | _page  | 1     |
      | _limit | 3     |
    When I send a GET request
    Then the response status code should be 200
    And the response body should be a non-empty list
    And the response field "0.id" should equal 1
    And the response should match the "users_list" schema

  Scenario: Retrieve a single user by id
    Given the API endpoint is "/users/1"
    When I send a GET request
    Then the response status code should be 200
    And the response field "id" should equal 1
    And the response field "username" should equal "Bret"
    And the response should match the "single_user" schema

  Scenario: Requesting a missing user returns not found
    Given the API endpoint is "/users/999999"
    When I send a GET request
    Then the response status code should be 404
    And the response should match the "empty_object" schema
