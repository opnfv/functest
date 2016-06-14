*** Settings ***
Documentation     Checking Subnets deleted in OpenStack are deleted also in OpenDaylight
Suite Setup       Create Session    OSSession     http://${NEUTRON}:9696    headers=${X-AUTH}
Suite Teardown    Delete All Sessions
Library           RequestsLibrary
Variables         ../../../variables/Variables.py

*** Variables ***
${ODLREST}       /controller/nb/v2/neutron/subnets
${OSREST}        /v2.0/subnets/${SUBNETID}
${data}          {"subnet":{"network_id":"${NETID}","ip_version":4,"cidr":"172.16.64.0/24","allocation_pools":[{"start":"172.16.64.20","end":"172.16.64.120"}]}}

*** Test Cases ***
Delete New subnet
    [Documentation]    Delete previously created subnet in OpenStack
    [Tags]    Delete Subnet OpenStack Neutron
    Log    ${data}
    ${resp}    delete    OSSession    ${OSREST}
    Should be Equal As Strings    ${resp.status_code}    204
    Log    ${resp.content}
    sleep    2

Check New subnet deleted
    [Documentation]    Check subnet deleted in OpenDaylight
    [Tags]    Check subnet deleted OpenDaylight
    Create Session    ODLSession    http://${CONTROLLER}:${PORT}    headers=${HEADERS}    auth=${AUTH}
    ${resp}    get    ODLSession    ${ODLREST}
    Should be Equal As Strings    ${resp.status_code}    200
    ${ODLResult}    To Json    ${resp.content}
    Set Suite Variable    ${ODLResult}
    Log    ${ODLResult}
    ${resp}    get    ODLSession    ${ODLREST}/${SUBNETID}
    Should be Equal As Strings    ${resp.status_code}    404
