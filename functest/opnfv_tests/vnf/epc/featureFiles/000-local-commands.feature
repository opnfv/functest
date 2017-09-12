    Feature: Local_Commands_Testing

    @local-commands
    Scenario: Local Commands testing
    Given all configured endpoints for SSH are connected successfully
    When I execute the command ifconfig in this system and check the presence of following strings in the response:
    | responseResult | existence               |
    | inet           | {string:nocase:present} |
    | UP             | {string:nocase:present} |
    | BROADCAST      | {string:nocase:present} |
    | RUNNING        | {string:nocase:present} |
    | MULTICAST      | {string:nocase:present} |
