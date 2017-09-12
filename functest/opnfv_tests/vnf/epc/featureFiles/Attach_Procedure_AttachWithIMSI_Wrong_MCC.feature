############################################################################################################################
#                                              Date: <31/08/2016> Version: <1.1>                                           #
############################################################################################################################

Feature:Attach_Procedure_AttachWithIMSI_Wrong_MCC

@attach-procedure @Attach_Procedure_AttachWithIMSI_Wrong_MCC @TS_24_301 @24_301_5_5 @24_301_5_5_1_2_2 @TS_24_368 @24_368_4 @24_368-5_4 @Series-0000

Scenario: Attach Procedure Failure due to wrong MCC.

Given all configured endpoints for SSH are connected successfully

Given the steps below will be executed at the end
When I stop S1AP simulator on node ABOT
When I run the SSH command "sudo service mme_gw restart" on node MME
Given the execution is paused for {abotprop.WAIT_10_SEC} seconds
Then the ending steps are complete

# set ABOT configuration
Given that I setup S1AP Simulator with default parameters specified in {abotprop.ABOT.EPC.Defaults} on node ABOT
Given that I setup S1AP Simulator with EPC parameter "ABOT.ENB.mobile_country_code=201" on node ABOT

# Execute ABOT S1AP Simulator
When I run S1AP simulator on node ABOT with 1 UE

Given the execution is paused for {abotprop.WAIT_10_SEC} seconds

# Validate Test Case Execution at Simulator
Then I receive S1AP response on node ABOT and verify the presence of all the following values:
| responseResult                    | existence               |
| Received s1 setup failure for MME | {string:nocase:present} |

