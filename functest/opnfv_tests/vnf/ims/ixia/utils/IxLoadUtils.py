#!/usr/bin/env python

# Copyright (c) 2017 IXIA and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import time
import logging

import requests

from functest.opnfv_tests.vnf.ims.ixia.utils import IxRestUtils


kActionStateFinished = 'finished'
kActionStatusSuccessful = 'Successful'
kActionStatusError = 'Error'
kTestStateUnconfigured = 'Unconfigured'

logger = logging.getLogger(__name__)


def stripApiAndVersionFromURL(url):

    # remove the slash (if any) at the beginning of the url

    if url[0] == '/':
        url = url[1:]

    urlElements = url.split('/')
    if 'api' in url:

        # strip the api/v0 part of the url

        urlElements = urlElements[2:]

    return '/'.join(urlElements)


def waitForActionToFinish(connection, replyObj, actionUrl):
    """
    This method waits for an action to finish executing. after a POST request
    is sent in order to start an action, The HTTP reply will contain,
    in the header, a 'location' field, that contains an URL.
    The action URL contains the status of the action. we perform a GET on that
    URL every 0.5 seconds until the action finishes with a success.
    If the action fails, we will throw an error and
    print the action's error message.
    """

    actionResultURL = replyObj.headers.get('location')
    if actionResultURL:
        actionResultURL = stripApiAndVersionFromURL(actionResultURL)
        actionFinished = False

        while not actionFinished:
            actionStatusObj = connection.httpGet(actionResultURL)

            if actionStatusObj.state == kActionStateFinished:
                if actionStatusObj.status == kActionStatusSuccessful:
                    actionFinished = True
                else:
                    errorMsg = "Error while executing action '%s'." \
                        % actionUrl

                    if actionStatusObj.status == kActionStatusError:
                        errorMsg += actionStatusObj.error

                    print errorMsg

                    sys.exit(1)
            else:
                time.sleep(0.1)


def performGenericOperation(connection, url, payloadDict):
    """
    This will perform a generic operation on the given url,
    it will wait for it to finish.
    """

    data = IxRestUtils.formatDictToJSONPayload(payloadDict)
    reply = connection.httpPost(url=url, data=data)

    waitForActionToFinish(connection, reply, url)

    return reply


def performGenericPost(connection, listUrl, payloadDict):
    """
    This will perform a generic POST method on a given url
    """

    data = IxRestUtils.formatDictToJSONPayload(payloadDict)

    reply = connection.httpPost(url=listUrl, data=data)
    try:
        newObjPath = reply.headers['location']
    except:
        raise Exception('Location header is not present. \
                        Please check if the action was created successfully.')

    newObjID = newObjPath.split('/')[-1]
    return newObjID


def performGenericDelete(connection, listUrl, payloadDict):
    """
    This will perform a generic DELETE method on a given url
    """

    data = IxRestUtils.formatDictToJSONPayload(payloadDict)

    reply = connection.httpDelete(url=listUrl, data=data)
    return reply


def performGenericPatch(connection, url, payloadDict):
    """
    This will perform a generic PATCH method on a given url
    """

    data = IxRestUtils.formatDictToJSONPayload(payloadDict)

    reply = connection.httpPatch(url=url, data=data)
    return reply


def createSession(connection, ixLoadVersion):
    """
    This method is used to create a new session.
    It will return the url of the newly created session
    """

    sessionsUrl = 'sessions'
    data = {'ixLoadVersion': ixLoadVersion}

    sessionId = performGenericPost(connection, sessionsUrl, data)

    newSessionUrl = '%s/%s' % (sessionsUrl, sessionId)
    startSessionUrl = '%s/operations/start' % newSessionUrl

    # start the session

    performGenericOperation(connection, startSessionUrl, {})

    logger.debug('Created session no %s' % sessionId)

    return newSessionUrl


def deleteSession(connection, sessionUrl):
    """
    This method is used to delete an existing session.
    """

    deleteParams = {}
    performGenericDelete(connection, sessionUrl, deleteParams)


def uploadFile(connection, url, fileName, uploadPath, overwrite=True):
    headers = {'Content-Type': 'multipart/form-data'}
    params = {'overwrite': overwrite, 'uploadPath': uploadPath}

    logger.debug('Uploading...')
    try:
        with open(fileName, 'rb') as f:
            resp = requests.post(url, data=f, params=params,
                                 headers=headers)
    except requests.exceptions.ConnectionError, e:
        raise Exception('Upload file failed. Received connection error. \
                        One common cause for this error is the size of the \
                        file to be uploaded.The web server sets a limit of 1GB\
                        for the uploaded file size. \
                        Received the following error: %s' % str(e))
    except IOError, e:
        raise Exception('Upload file failed. Received IO error: %s'
                        % str(e))
    except Exception:
        raise Exception('Upload file failed. Received the following error: %s'
                        % str(e))
    else:
        logger.debug('Upload file finished.')
        logger.debug('Response status code %s' % resp.status_code)
        logger.debug('Response text %s' % resp.text)


def loadRepository(connection, sessionUrl, rxfFilePath):
    """
    This method will perform a POST request to load a repository.
    """

    loadTestUrl = '%s/ixload/test/operations/loadTest' % sessionUrl
    data = {'fullPath': rxfFilePath}

    performGenericOperation(connection, loadTestUrl, data)


def saveRxf(connection, sessionUrl, rxfFilePath):
    """
    This method saves the current rxf to the disk of the machine on
    which the IxLoad instance is running.
    """

    saveRxfUrl = '%s/ixload/test/operations/saveAs' % sessionUrl
    rxfFilePath = rxfFilePath.replace('\\', '\\\\')
    data = {'fullPath': rxfFilePath, 'overWrite': 1}

    performGenericOperation(connection, saveRxfUrl, data)


def runTest(connection, sessionUrl):
    """
    This method is used to start the currently loaded test.
    After starting the 'Start Test' action, wait for the action to complete.
    """

    startRunUrl = '%s/ixload/test/operations/runTest' % sessionUrl
    data = {}

    performGenericOperation(connection, startRunUrl, data)


def getTestCurrentState(connection, sessionUrl):
    """
    This method gets the test current state.
    (for example - running, unconfigured, ..)
    """

    activeTestUrl = '%s/ixload/test/activeTest' % sessionUrl
    testObj = connection.httpGet(activeTestUrl)

    return testObj.currentState


def getTestRunError(connection, sessionUrl):
    """
    This method gets the error that appeared during the last test run.
    If no error appeared (the test ran successfully),
    the return value will be 'None'.
    """

    activeTestUrl = '%s/ixload/test/activeTest' % sessionUrl
    testObj = connection.httpGet(activeTestUrl)

    return testObj.testRunError


def waitForTestToReachUnconfiguredState(connection, sessionUrl):
    """
    This method waits for the current test to reach the 'Unconfigured' state.
    """

    while getTestCurrentState(connection, sessionUrl) \
            != kTestStateUnconfigured:
        time.sleep(0.1)


def pollStats(connection, sessionUrl, watchedStatsDict, pollingInterval=4):
    """
    This method is used to poll the stats.
    Polling stats is per request but this method does a continuous poll.
    """

    statSourceList = watchedStatsDict.keys()
    statsDict = {}

    collectedTimestamps = {}
    testIsRunning = True

    # check stat sources

    for statSource in statSourceList[:]:
        statSourceUrl = '%s/ixload/stats/%s/values' % (sessionUrl, statSource)
        statSourceReply = connection.httpRequest('GET', statSourceUrl)
        if statSourceReply.status_code != 200:
            logger.debug("Warning - Stat source '%s' does not exist. \
                         Will ignore it." % statSource)
            statSourceList.remove(statSource)

    # check the test state, and poll stats while the test is still running

    while testIsRunning:

        # the polling interval is configurable.
        # by default, it's set to 4 seconds

        time.sleep(pollingInterval)

        for statSource in statSourceList:
            valuesUrl = '%s/ixload/stats/%s/values' % (sessionUrl, statSource)

            valuesObj = connection.httpGet(valuesUrl)
            valuesDict = valuesObj.getOptions()

            # get just the new timestamps - that were not previously
            # retrieved in another stats polling iteration

            newTimestamps = [int(timestamp) for timestamp in
                             valuesDict.keys() if timestamp
                             not in collectedTimestamps.get(statSource,
                             [])]
            newTimestamps.sort()

            for timestamp in newTimestamps:
                timeStampStr = str(timestamp)

                collectedTimestamps.setdefault(
                    statSource, []).append(timeStampStr)

                timestampDict = statsDict.setdefault(
                    statSource, {}).setdefault(timestamp, {})

                # save the values for the current timestamp,
                # and later print them

                logger.info(' -- ')
                for (caption, value) in \
                        valuesDict[timeStampStr].getOptions().items():
                    if caption in watchedStatsDict[statSource]:
                        logger.info(' %s -> %s' % (caption, value))
                        timestampDict[caption] = value

        testIsRunning = getTestCurrentState(connection, sessionUrl) \
            == 'Running'

    logger.debug('Stopped receiving stats.')
    return timestampDict


def clearChassisList(connection, sessionUrl):
    """
    This method is used to clear the chassis list.
    After execution no chassis should be available in the chassisListself.
    """

    chassisListUrl = '%s/ixload/chassischain/chassisList' % sessionUrl
    deleteParams = {}
    performGenericDelete(connection, chassisListUrl, deleteParams)


def configureLicenseServer(connection, sessionUrl, licenseServerIp):
    """
    This method is used to clear the chassis list.
    After execution no chassis should be available in the chassisList.
    """

    chassisListUrl = '%s/ixload/preferences' % sessionUrl
    patchParams = {'licenseServer': licenseServerIp}
    performGenericPatch(connection, chassisListUrl, patchParams)


def addChassisList(connection, sessionUrl, chassisList):
    """
    This method is used to add one or more chassis to the chassis list.
    """

    chassisListUrl = '%s/ixload/chassisChain/chassisList' % sessionUrl

    for chassisName in chassisList:
        data = {'name': chassisName}
        chassisId = performGenericPost(connection, chassisListUrl, data)

        # refresh the chassis

        refreshConnectionUrl = '%s/%s/operations/refreshConnection' \
            % (chassisListUrl, chassisId)
        performGenericOperation(connection, refreshConnectionUrl, {})


def assignPorts(connection, sessionUrl, portListPerCommunity):
    """
    This method is used to assign ports from a connected chassis
    to the required NetTraffics.
    """

    communtiyListUrl = '%s/ixload/test/activeTest/communityList' \
        % sessionUrl

    communityList = connection.httpGet(url=communtiyListUrl)

    for community in communityList:
        portListForCommunity = portListPerCommunity.get(community.name)

        portListUrl = '%s/%s/network/portList' % (communtiyListUrl,
                                                  community.objectID)

        if portListForCommunity:
            for portTuple in portListForCommunity:
                (chassisId, cardId, portId) = portTuple
                paramDict = {'chassisId': chassisId, 'cardId': cardId,
                             'portId': portId}

                performGenericPost(connection, portListUrl, paramDict)
