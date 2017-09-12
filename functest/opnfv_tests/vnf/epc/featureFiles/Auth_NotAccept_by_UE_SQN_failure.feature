    ############################################################################################################################
    #                                              Date: <13/01/2017> Version: <1.1>                                           #
    ############################################################################################################################


    Feature:Auth_NotAccept_by_UE_SQN_failure

    @authentication-procedure @Auth_NotAccept_by_UE_SQN_failure  @TS_24_301 @24_301_5_4_2_6 @24_301_5_4_2_7 @negTCs @Series-0004

    Scenario: UE receives an AUTHENTICATION REQUEST message with SQN out of range. UE sends an AUTHENTICATION FAILURE message to the network, with EMM cause "synch failure" and a re-synchronization token. Now UE receives a new correct AUTHENTICATION REQUEST message while T3420 is running. Finally UE sends a correct AUTHENTICATION RESPONSE message.

    Given all configured endpoints for SSH are connected successfully

    Given the steps below will be executed at the end
    When I stop S1AP simulator on node ABOT
    When I run the SSH command "sudo service mme_gw restart" on node MME
    Given that I setup S1AP Simulator with UE parameter "ABOT.UE.CONFIG.SECURITY.SYNC_FAILURE=false" on node ABOT
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.AttachWithImsi=true" on node ABOT
    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds
    Then the ending steps are complete

    # set ABOT configuration
    Given that I setup S1AP Simulator with default parameters specified in {abotprop.ABOT.EPC.Defaults} on node ABOT
    Given that I setup S1AP Simulator with UE parameter "ABOT.UE.CONFIG.SECURITY.SYNC_FAILURE=true" on node ABOT
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.AttachWithImsi=false" on node ABOT

    # Execute ABOT S1AP Simulator
    When I run S1AP simulator on node ABOT with 1 UE

    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds
    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds

    # Validate Test Case Execution at Simulator
    Then I receive S1AP response on node ABOT and verify the presence of all the following values:
    | responseResult                                 | existence               |
    | Send Attach Request message with GUTI          | {string:nocase:present} |
    | Received Identity Request message              | {string:nocase:present} |
    | Identification requested type = IMSI           | {string:nocase:present} |
    | Send Identity Response message                 | {string:nocase:present} |
    | Received Authentication Request message        | {string:nocase:present} |
    | Send Authentication Failure message (cause=21) | {string:nocase:present} |
    | Received Authentication Request message        | {string:nocase:present} |
    | Send Authentication Response message           | {string:nocase:present} |
    | Received Security Mode Command message         | {string:nocase:present} |
    | Send Security Mode Complete message            | {string:nocase:present} |
    | Received Attach Accept message                 | {string:nocase:present} |
