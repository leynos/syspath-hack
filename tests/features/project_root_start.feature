Feature: Explicit project root search starts

  Scenario: Finding a project root from an explicit start directory
    Given a project root with marker "pyproject.toml"
    And a nested start directory beneath the project root
    And I am in a different working directory
    When I search for the project root from the explicit start directory
    Then the located project root is the one containing the marker

  Scenario: Adding a project root from an explicit start directory
    Given a project root with marker "pyproject.toml"
    And a nested start directory beneath the project root
    And I am in a different working directory
    And sys.path is empty
    When I add the project root from the explicit start directory
    Then sys.path begins with the project root
