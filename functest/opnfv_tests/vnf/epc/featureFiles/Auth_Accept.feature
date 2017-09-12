    ############################################################################################################################
    #                                              Date: <13/01/2017> Version: <1.1>                                           #
    ############################################################################################################################


    Feature:Auth_Accept

    @authentication-procedure @Auth_Accept  @TS_24_301 @24_301_5_4_2_1 @24_301_5_4_2_3 @33_401_6_1_1 @Series-0004

    Scenario: UE receives an AUTHENTICATION REQUEST message. UE responds with a correct AUTHENTICATION RESPONSE message and establishes correct
    EPS security context.

    Given all configured endpoints for SSH are connected successfully

    Given the steps below will be executed at the end
    When I stop S1AP simulator on node ABOT
    When I run the SSH command "sudo service mme_gw restart" on node MME
    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds
    Then the ending steps are complete

    # Set ABOT configuration
    Given that I setup S1AP Simulator with default parameters specified in {abotprop.ABOT.EPC.Defaults} on node ABOT
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.AttachWithImsi=false" on node ABOT

    # Execute ABOT S1AP Simulator
    When I run S1AP simulator on node ABOT with 1 UE

    # Wait for execution to complete before checking results
    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds

    # Validate Test Case Execution at Simulator
    Then I receive S1AP response on node ABOT and verify the presence of all the following values:
    | responseResult                                 | existence               |
    | Send Attach Request message with GUTI          | {string:nocase:present} |
    | Received Identity Request message              | {string:nocase:present} |
    | Identification requested type = IMSI           | {string:nocase:present} |
    | Send Identity Response message                 | {string:nocase:present} |
    | Received Authentication Request message        | {string:nocase:present} |
    | Send Authentication Response message           | {string:nocase:present} |
    | Received Security Mode Command message         | {string:nocase:present} |
    | Send Security Mode Complete message            | {string:nocase:present} |
    | Received Attach Accept message                 | {string:nocase:present} |



