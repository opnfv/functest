#!/usr/bin/env python

# Copyright (c) 2017 IXIA and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import httplib2
import json
import logging


okStates = [200, 201, 202]
states = [
    'Queued',
    'In Progress',
    'Manual Step Required',
    'Error',
    'Finished',
    'Aborted',
    'Retried',
    'IRebooting',
    'Force Continue',
    'Pending',
    ]
notStartedState = 'Not_Started'
errorStates = ['Error', 'Aborted', 'Force Continue']
finishedStates = ['Manual Step Required', 'Finished']

logger = logging.getLogger(__name__)


class TestFailedError(Exception):
    pass


class ChassisRestAPI:
    @staticmethod
    def postWithPayload(loginUrl, payload=None):
        urlHeadersJson = {'content-type': 'application/json'}
        try:
            h = httplib2.Http('.cache',
                              disable_ssl_certificate_validation=True)
            if payload is None:
                logger.debug('POST: ' + loginUrl)
                (response, content) = h.request(loginUrl, 'POST', '',
                                                urlHeadersJson)
                logger.debug(content)
            else:
                logger.debug('POST: ' + loginUrl + ' <- Data: ' + str(payload))
                (response, content) = h.request(loginUrl, 'POST',
                                                body=payload,
                                                headers=urlHeadersJson)
                logger.debug(response)
                logger.debug(content)
        except Exception, e:
            raise Exception('Got an error code: ', e)
        return content

    @staticmethod
    def postWithPayloadAndHeaders(loginUrl, urlHeadersJson,
                                  payload=None):
        try:
            h = httplib2.Http('.cache',
                              disable_ssl_certificate_validation=True)
            if payload is None:
                logger.debug('POST: ' + loginUrl)
                (response, content) = h.request(loginUrl, 'POST', '',
                                                urlHeadersJson)
            else:
                logger.debug('POST: ' + loginUrl + ' <- Data: ' + str(payload))
                (response, content) = h.request(loginUrl, 'POST',
                                                body=payload,
                                                headers=urlHeadersJson)
        except Exception, e:
            raise Exception('Got an error code: ', e)
        return content

    @staticmethod
    def postOperation(url, apiKey, payload=''):
        urlHeadersJson = {'content-type': 'application/json',
                          'X-Api-Key': '%s' % str(apiKey)}
        try:
            h = httplib2.Http('.cache',
                              disable_ssl_certificate_validation=True)
            if payload is None:
                logger.debug('POST: ' + url)
                (response, content) = h.request(url, 'POST',
                                                json.dumps(payload),
                                                urlHeadersJson)
            else:
                logger.debug('POST: ' + url + ' <- Data: ' + str(payload))
                (response, content) = h.request(url, 'POST',
                                                json.dumps(payload),
                                                headers=urlHeadersJson)
        except Exception, e:
            raise Exception('Got an error code: ', e)
        return content

    @staticmethod
    def patch(url, payload, apiKey):
        urlHeadersJson = {'content-type': 'application/json',
                          'X-Api-Key': '%s' % str(apiKey)}
        try:
            h = httplib2.Http('.cache',
                              disable_ssl_certificate_validation=True)
            logger.debug('PATCH: ' + url + ' <-- Attribute: ' +
                         str(payload))
            (response, content) = h.request(url, 'PATCH',
                                            json.dumps(payload),
                                            urlHeadersJson)
        except Exception, e:

            # print (response, content)

            raise Exception('Got an error code: ', e)
        return content

    @staticmethod
    def delete(url, apiKey):
        urlHeadersJson = {'content-type': 'application/json',
                          'X-Api-Key': '%s' % str(apiKey)}
        try:
            h = httplib2.Http('.cache',
                              disable_ssl_certificate_validation=True)
            (response, content) = h.request(url, 'DELETE', '', urlHeadersJson)
            logger.debug('DELETE: ' + url)
        except Exception, e:
            raise Exception('Got an error code: ', e)
        if response.status not in okStates:
            raise TestFailedError(json.loads(content)['error'])
        return json.loads(content)

    @staticmethod
    def getWithHeaders(url, apiKey):
        urlHeadersJson = {'content-type': 'application/json',
                          'X-Api-Key': '%s' % str(apiKey)}
        try:
            h = httplib2.Http('.cache',
                              disable_ssl_certificate_validation=True)
            logger.debug('GET: ' + url)
            (response, content) = h.request(url, 'GET', '', urlHeadersJson)
        except Exception, e:
            raise Exception('Got an error code: ', e)
        if response.status not in okStates:
            raise TestFailedError(json.loads(content)['error'])
        output = json.loads(content)
        return output
