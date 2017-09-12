    ############################################################################################################################
    #                                              Date: <13/12/2016> Version: <1.1>                                           #
    ############################################################################################################################

    Feature:Auth_NotAccept_by_UE_GUTIattachMAC_code_failure

    @authentication-procedure @Auth_NotAccept_by_UE_GUTIattach_MAC_code_failure @TS_24_301 @24_301_5_4_2_6 @24_301_5_4_2_7 @negTCs @Series-0002

    Scenario: UE received invalid MAC code in AUTN parameter in the AUTHENTICATION REQUEST message. Authentication not accepted by the UE when attach with GUTI. UE responds the Authentication failure message with EMM cause (reject cause) #20 "MAC failure".

    Given all configured endpoints for SSH are connected successfully

    Given the steps below will be executed at the end
    When I stop S1AP simulator on node ABOT
    When I run the SSH command "sudo service mme_gw restart" on node MME
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.AttachWithImsi=true" on node ABOT
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.USIM_API_K=\"8BAF473F2F8FD09487CCCBD7097C6862\"" on node ABOT
    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds
    Then the ending steps are complete

    # set ABOT configuration
    Given that I setup S1AP Simulator with default parameters specified in {abotprop.ABOT.EPC.Defaults} on node ABOT
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.AttachWithImsi=false" on node ABOT

    # CORRECT K_VALUE is 8BAF473F2F8FD09487CCCBD7097C6862 WRONG K_VALUE fec86ba6eb707ed08905757b1bb44b8f
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.USIM_API_K=\"fec86ba6eb707ed08905757b1bb44b8f\"" on node ABOT

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
    | Send Authentication Failure message (cause=20) | {string:nocase:present} |
    | Received Authentication Reject message         | {string:nocase:present} |
    | Authentication not accepted by the network     | {string:nocase:present} |

