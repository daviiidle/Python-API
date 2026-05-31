Feature: Posts API
  As a QA Automation Engineer
  I want to validate post endpoints
  So that create, update, delete, and negative API behavior is covered

  Scenario: Retrieve a list of posts
    Given the API endpoint is "/posts"
    And the query parameters are
      | key    | value |
      | _limit | 5     |
    When I send a GET request
    Then the response status code should be 200
    And the response body should be a non-empty list
    And the response should match the "posts_list" schema

  Scenario: Create a post using dynamic test data
    Given the API endpoint is "/posts"
    And I have a dynamic post payload
    When I send a POST request
    Then the response status code should be 201
    And the response should include the request payload
    And the response should match the "created_post" schema

  Scenario: Update an existing post
    Given the API endpoint is "/posts/1"
    And the request payload is
      | key    | value                           |
      | id     | 1                               |
      | title  | Updated API automation title    |
      | body   | Updated by Behave and Requests. |
      | userId | 1                               |
    When I send a PUT request
    Then the response status code should be 200
    And the response should include the request payload
    And the response should match the "single_post" schema

  Scenario: Delete an existing post
    Given the API endpoint is "/posts/1"
    When I send a DELETE request
    Then the response status code should be 200
    And the response should match the "empty_object" schema

  Scenario: Requesting a missing post returns not found
    Given the API endpoint is "/posts/999999"
    When I send a GET request
    Then the response status code should be 404
    And the response should match the "empty_object" schema
