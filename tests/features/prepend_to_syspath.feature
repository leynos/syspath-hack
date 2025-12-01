Feature: Prepending paths keeps the CWD sentinel

  Scenario: Prepending current working directory retains leading blank entry
    Given I am in a temporary working directory
    And sys.path starts with a blank entry and "other"
    When I prepend the current working directory to sys.path
    Then sys.path lists the current working directory first and preserves the blank entry
