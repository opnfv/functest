#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Unitary test for energy module."""
# pylint: disable=unused-argument
import logging
import unittest

import mock

from functest.energy.energy import EnergyRecorder
import functest.energy.energy as energy
from functest.utils.constants import CONST
import requests

CASE_NAME = "UNIT_TEST_CASE"
STEP_NAME = "UNIT_TEST_STEP"

PREVIOUS_SCENARIO = "previous_scenario"
PREVIOUS_STEP = "previous_step"


class MockHttpResponse(object):  # pylint: disable=too-few-public-methods
    """Mock response for Energy recorder API."""

    def __init__(self, text, status_code):
        """Create an instance of MockHttpResponse."""
        self.text = text
        self.status_code = status_code


API_OK = MockHttpResponse(
    '{"status": "OK"}',
    200
)
API_KO = MockHttpResponse(
    '{"message": "API-KO"}',
    500
)

RECORDER_OK = MockHttpResponse(
    '{"environment": "UNIT_TEST",'
    ' "step": "string",'
    ' "scenario": "' + CASE_NAME + '"}',
    200
)
RECORDER_KO = MockHttpResponse(
    '{"message": "An unhandled API exception occurred (MOCK)"}',
    500
)
RECORDER_NOT_FOUND = MockHttpResponse(
    '{"message": "Recorder not found (MOCK)"}',
    404
)


def config_loader_mock(config_key):
    """Return mocked config values."""
    if config_key == "energy_recorder.api_url":
        return "http://pod-uri:8888"
    elif config_key == "energy_recorder.api_user":
        return "user"
    elif config_key == "energy_recorder.api_password":
        return "password"


def config_loader_mock_no_creds(config_key):
    """Return mocked config values."""
    if config_key == "energy_recorder.api_url":
        return "http://pod-uri:8888"
    elif config_key == "energy_recorder.api_user":
        return ""
    elif config_key == "energy_recorder.api_password":
        return ""


# pylint: disable=too-many-public-methods
class EnergyRecorderTest(unittest.TestCase):
    """Energy module unitary test suite."""

    case_name = CASE_NAME
    request_headers = {'content-type': 'application/json'}
    returned_value_to_preserve = "value"
    exception_message_to_preserve = "exception_message"

    @mock.patch('functest.energy.energy.requests.post',
                return_value=RECORDER_OK)
    def test_start(self, post_mock=None, get_mock=None):
        """EnergyRecorder.start method (regular case)."""
        self.test_load_config()
        self.assertTrue(EnergyRecorder.start(self.case_name))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @mock.patch('functest.energy.energy.requests.post',
                side_effect=Exception("Internal execution error (MOCK)"))
    def test_start_error(self, post_mock=None):
        """EnergyRecorder.start method (error in method)."""
        self.test_load_config()
        self.assertFalse(EnergyRecorder.start(self.case_name))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @mock.patch('functest.energy.energy.EnergyRecorder.load_config',
                side_effect=Exception("Internal execution error (MOCK)"))
    def test_start_exception(self, conf_loader_mock=None):
        """EnergyRecorder.start test with exception during execution."""
        start_status = EnergyRecorder.start(CASE_NAME)
        self.assertFalse(start_status)

    @mock.patch('functest.energy.energy.requests.post',
                return_value=RECORDER_KO)
    def test_start_api_error(self, post_mock=None):
        """EnergyRecorder.start method (API error)."""
        self.test_load_config()
        self.assertFalse(EnergyRecorder.start(self.case_name))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @mock.patch('functest.energy.energy.requests.post',
                return_value=RECORDER_OK)
    def test_set_step(self, post_mock=None):
        """EnergyRecorder.set_step method (regular case)."""
        self.test_load_config()
        self.assertTrue(EnergyRecorder.set_step(STEP_NAME))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"] + "/step",
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @mock.patch('functest.energy.energy.requests.post',
                return_value=RECORDER_KO)
    def test_set_step_api_error(self, post_mock=None):
        """EnergyRecorder.set_step method (API error)."""
        self.test_load_config()
        self.assertFalse(EnergyRecorder.set_step(STEP_NAME))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"] + "/step",
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @mock.patch('functest.energy.energy.requests.post',
                side_effect=Exception("Internal execution error (MOCK)"))
    def test_set_step_error(self, post_mock=None):
        """EnergyRecorder.set_step method (method error)."""
        self.test_load_config()
        self.assertFalse(EnergyRecorder.set_step(STEP_NAME))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"] + "/step",
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @mock.patch('functest.energy.energy.EnergyRecorder.load_config',
                side_effect=requests.exceptions.ConnectionError())
    def test_set_step_connection_error(self, conf_loader_mock=None):
        """EnergyRecorder.start test with exception during execution."""
        step_status = EnergyRecorder.set_step(STEP_NAME)
        self.assertFalse(step_status)

    @mock.patch('functest.energy.energy.requests.delete',
                return_value=RECORDER_OK)
    def test_stop(self, delete_mock=None):
        """EnergyRecorder.stop method (regular case)."""
        self.test_load_config()
        self.assertTrue(EnergyRecorder.stop())
        delete_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @mock.patch('functest.energy.energy.requests.delete',
                return_value=RECORDER_KO)
    def test_stop_api_error(self, delete_mock=None):
        """EnergyRecorder.stop method (API Error)."""
        self.test_load_config()
        self.assertFalse(EnergyRecorder.stop())
        delete_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @mock.patch('functest.energy.energy.requests.delete',
                side_effect=Exception("Internal execution error (MOCK)"))
    def test_stop_error(self, delete_mock=None):
        """EnergyRecorder.stop method (method error)."""
        self.test_load_config()
        self.assertFalse(EnergyRecorder.stop())
        delete_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            headers=self.request_headers,
            timeout=EnergyRecorder.CONNECTION_TIMEOUT
        )

    @energy.enable_recording
    def __decorated_method(self):
        """Call with to energy recorder decorators."""
        return self.returned_value_to_preserve

    @energy.enable_recording
    def __decorated_method_with_ex(self):
        """Call with to energy recorder decorators."""
        raise Exception(self.exception_message_to_preserve)

    @mock.patch("functest.energy.energy.EnergyRecorder.get_current_scenario",
                return_value=None)
    @mock.patch("functest.energy.energy.EnergyRecorder")
    def test_decorators(self,
                        recorder_mock=None,
                        cur_scenario_mock=None):
        """Test energy module decorators."""
        self.__decorated_method()
        calls = [mock.call.start(self.case_name),
                 mock.call.stop()]
        recorder_mock.assert_has_calls(calls)

    @mock.patch("functest.energy.energy.EnergyRecorder.get_current_scenario",
                return_value={"scenario": PREVIOUS_SCENARIO,
                              "step": PREVIOUS_STEP})
    @mock.patch("functest.energy.energy.EnergyRecorder")
    @mock.patch("functest.utils.functest_utils.get_functest_config",
                side_effect=config_loader_mock)
    def test_decorators_with_previous(self,
                                      loader_mock=None,
                                      recorder_mock=None,
                                      cur_scenario_mock=None):
        """Test energy module decorators."""
        CONST.__setattr__('NODE_NAME', 'MOCK_POD')
        self.__decorated_method()
        calls = [mock.call.start(self.case_name),
                 mock.call.submit_scenario(PREVIOUS_SCENARIO,
                                           PREVIOUS_STEP)]
        recorder_mock.assert_has_calls(calls, True)

    def test_decorator_preserve_return(self):
        """Test that decorator preserve method returned value."""
        self.test_load_config()
        self.assertTrue(
            self.__decorated_method() == self.returned_value_to_preserve
        )

    @mock.patch(
        "functest.energy.energy.finish_session")
    def test_decorator_preserve_ex(self, finish_mock=None):
        """Test that decorator preserve method exceptions."""
        self.test_load_config()
        with self.assertRaises(Exception) as context:
            self.__decorated_method_with_ex()
        self.assertTrue(
            self.exception_message_to_preserve in str(context.exception)
        )
        self.assertTrue(finish_mock.called)

    @mock.patch("functest.utils.functest_utils.get_functest_config",
                side_effect=config_loader_mock)
    @mock.patch("functest.energy.energy.requests.get",
                return_value=API_OK)
    def test_load_config(self, loader_mock=None, get_mock=None):
        """Test load config."""
        CONST.__setattr__('NODE_NAME', 'MOCK_POD')
        EnergyRecorder.energy_recorder_api = None
        EnergyRecorder.load_config()

        self.assertEquals(
            EnergyRecorder.energy_recorder_api["auth"],
            ("user", "password")
        )
        self.assertEquals(
            EnergyRecorder.energy_recorder_api["uri"],
            "http://pod-uri:8888/recorders/environment/MOCK_POD"
        )

    @mock.patch("functest.utils.functest_utils.get_functest_config",
                side_effect=config_loader_mock_no_creds)
    @mock.patch("functest.energy.energy.requests.get",
                return_value=API_OK)
    def test_load_config_no_creds(self, loader_mock=None, get_mock=None):
        """Test load config without creds."""
        CONST.__setattr__('NODE_NAME', 'MOCK_POD')
        EnergyRecorder.energy_recorder_api = None
        EnergyRecorder.load_config()
        self.assertEquals(EnergyRecorder.energy_recorder_api["auth"], None)
        self.assertEquals(
            EnergyRecorder.energy_recorder_api["uri"],
            "http://pod-uri:8888/recorders/environment/MOCK_POD"
        )

    @mock.patch("functest.utils.functest_utils.get_functest_config",
                return_value=None)
    @mock.patch("functest.energy.energy.requests.get",
                return_value=API_OK)
    def test_load_config_ex(self, loader_mock=None, get_mock=None):
        """Test load config with exception."""
        CONST.__setattr__('NODE_NAME', 'MOCK_POD')
        with self.assertRaises(AssertionError):
            EnergyRecorder.energy_recorder_api = None
            EnergyRecorder.load_config()
        self.assertEquals(EnergyRecorder.energy_recorder_api, None)

    @mock.patch("functest.utils.functest_utils.get_functest_config",
                side_effect=config_loader_mock)
    @mock.patch("functest.energy.energy.requests.get",
                return_value=API_KO)
    def test_load_config_api_ko(self, loader_mock=None, get_mock=None):
        """Test load config with API unavailable."""
        CONST.__setattr__('NODE_NAME', 'MOCK_POD')
        EnergyRecorder.energy_recorder_api = None
        EnergyRecorder.load_config()
        self.assertEquals(EnergyRecorder.energy_recorder_api["available"],
                          False)

    @mock.patch("functest.utils.functest_utils.get_functest_config",
                return_value=None)
    @mock.patch('functest.energy.energy.requests.get',
                return_value=RECORDER_OK)
    def test_get_current_scenario(self, loader_mock=None, get_mock=None):
        """Test get_current_scenario."""
        CONST.__setattr__('NODE_NAME', 'MOCK_POD')
        self.test_load_config()
        scenario = EnergyRecorder.get_current_scenario()
        self.assertTrue(scenario is not None)

    @mock.patch('functest.energy.energy.requests.get',
                return_value=RECORDER_NOT_FOUND)
    def test_current_scenario_not_found(self, get_mock=None):
        """Test get current scenario not existing."""
        CONST.__setattr__('NODE_NAME', 'MOCK_POD')
        self.test_load_config()
        scenario = EnergyRecorder.get_current_scenario()
        self.assertTrue(scenario is None)

    @mock.patch('functest.energy.energy.requests.get',
                return_value=RECORDER_KO)
    def test_current_scenario_api_error(self, get_mock=None):
        """Test get current scenario with API error."""
        CONST.__setattr__('NODE_NAME', 'MOCK_POD')
        self.test_load_config()
        scenario = EnergyRecorder.get_current_scenario()
        self.assertTrue(scenario is None)

    @mock.patch('functest.energy.energy.EnergyRecorder.load_config',
                side_effect=Exception("Internal execution error (MOCK)"))
    def test_current_scenario_exception(self, get_mock=None):
        """Test get current scenario with exception."""
        scenario = EnergyRecorder.get_current_scenario()
        self.assertTrue(scenario is None)

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
