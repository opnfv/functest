*** Settings ***
Documentation     Checking Port deleted in OpenStack are deleted also in OpenDaylight
Suite Setup       Create Session    OSSession     http://${NEUTRON}:9696    headers=${X-AUTH}
Suite Teardown    Delete All Sessions
Library           SSHLibrary
Library           Collections
Library           OperatingSystem
Library           ../../../libraries/RequestsLibrary.py
Library           ../../../libraries/Common.py
Variables         ../../../variables/Variables.py

*** Variables ***
${ODLREST}       /controller/nb/v2/neutron/ports
${OSREST}        /v2.0/ports/${PORTID}
${data}       {"port":{"network_id":"${NETID}","admin_state_up": true}}

*** Test Cases ***
Delete New Port
    [Documentation]    Delete previously created port in OpenStack
    [Tags]    Delete port OpenStack Neutron
    Log    ${data}
    ${resp}    delete    OSSession    ${OSREST}
    Should be Equal As Strings    ${resp.status_code}    204
    Log    ${resp.content}
    sleep    2

Check Port Deleted
    [Documentation]    Check port deleted in OpenDaylight
    [Tags]    Check port deleted OpenDaylight
    Create Session    ODLSession    http://${CONTROLLER}:${PORT}    headers=${HEADERS}    auth=${AUTH}
    ${resp}    get    ODLSession    ${ODLREST}
    Should be Equal As Strings    ${resp.status_code}    200
    ${ODLResult}    To Json    ${resp.content}
    Set Suite Variable    ${ODLResult}
    Log    ${ODLResult}
    ${resp}    get    ODLSession    ${ODLREST}/${PORTID}
    Should be Equal As Strings    ${resp.status_code}    404
