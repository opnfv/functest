*** Settings ***
Documentation     Checking Network deleted in OpenStack are deleted also in OpenDaylight
Suite Setup       Create Session    OSSession     http://${NEUTRON}:9696    headers=${X-AUTH}
Suite Teardown    Delete All Sessions
Library           RequestsLibrary
Variables         ../../../variables/Variables.py

*** Variables ***
${ODLREST}       /controller/nb/v2/neutron/networks
${OSREST}        /v2.0/networks/${NETID}
${postNet}       {"network":{"name":"odl_network","admin_state_up":true}}

*** Test Cases ***
Delete Network
    [Documentation]    Delete network in OpenStack
    [Tags]    Delete Network OpenStack Neutron
    Log    ${postNet}
    ${resp}    delete    OSSession    ${OSREST}
    Should be Equal As Strings    ${resp.status_code}    204
    Log    ${resp.content}
    sleep    2

Check Network deleted
    [Documentation]    Check network deleted in OpenDaylight
    [Tags]    Check  Network OpenDaylight
    Create Session    ODLSession    http://${CONTROLLER}:${PORT}    headers=${HEADERS}    auth=${AUTH}
    ${resp}    get    ODLSession    ${ODLREST}
    Should be Equal As Strings    ${resp.status_code}    200
    ${ODLResult}    To Json    ${resp.content}
    Set Suite Variable    ${ODLResult}
    Log    ${ODLResult}
    ${resp}    get    ODLSession    ${ODLREST}/${NetID}
    Should be Equal As Strings    ${resp.status_code}    404
