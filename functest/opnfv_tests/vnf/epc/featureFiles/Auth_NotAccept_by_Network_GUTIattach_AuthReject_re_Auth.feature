    ############################################################################################################################
    #                                              Date: <22/11/2016> Version: <1.1>                                           #
    ############################################################################################################################


    Feature:Auth_NotAccept_by_Network_GUTIattach_AuthReject_re_Auth

    @authentication-procedure @Auth_NotAccept_by_Network_GUTIattach_AuthReject_re_Auth @TS_24_301 @24_301_5_3_3 @24_301_5_5_1_2_2 @24_301_5_5_1_2_4 @24_301_6_5_1_2 @24_301_9_9_3_33 @TS_36_304 @36_304_4_3 @negTCs @Series-0001

    Scenario: Authentication not accepted by the network when attach with GUTI, Authentication reject when RES is different from UE and MME. IMSI given by the UE during the identification procedure is same from the IMSI the network had associated with the GUTI.

    Given all configured endpoints for SSH are connected successfully

    Given the steps below will be executed at the end
    When I stop S1AP simulator on node ABOT
    When I run the SSH command "sudo service mme_gw restart" on node MME
    #RES is restored to 0x00 in teardown process
    Given that I setup S1AP Simulator with UE parameter "ABOT.UE.CONFIG.SECURITY.RES=0x00" on node ABOT
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.AttachWithImsi=true" on node ABOT
    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds
    Then the ending steps are complete

    # set ABOT configuration
    Given that I setup S1AP Simulator with default parameters specified in {abotprop.ABOT.EPC.Defaults} on node ABOT
    Given that I setup S1AP Simulator with USIM parameter "ABOT.UE.USIM.AttachWithImsi=false" on node ABOT
    # set the value of RES parameter (other than 0x00) manually in Authentication Response message which is sent from UE to MME
    Given that I setup S1AP Simulator with UE parameter "ABOT.UE.CONFIG.SECURITY.RES=0xFF" on node ABOT


    # Execute ABOT S1AP Simulator
    When I run S1AP simulator on node ABOT with 1 UE

    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds
    Given the execution is paused for {abotprop.WAIT_10_SEC} seconds

    # Validate Test Case Execution at Simulator
    Then I receive S1AP response on node ABOT and verify the presence of all the following values:
    | responseResult                             | existence               |
    | Send Attach Request message with GUTI      | {string:nocase:present} |
    | Received Identity Request message          | {string:nocase:present} |
    | Identification requested type = IMSI       | {string:nocase:present} |
    | Send Identity Response message             | {string:nocase:present} |
    | Received Authentication Request message    | {string:nocase:present} |
    | Send Authentication Response message       | {string:nocase:present} |
    | Received Authentication Reject message     | {string:nocase:present} |
    | Authentication not accepted by the network | {string:nocase:present} |

