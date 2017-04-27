#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Unitary test for energy module."""

import logging
import unittest

import mock

from functest.energy.energy import EnergyRecorder
import functest.energy.energy as energy


CASE_NAME = "UNIT_TEST_CASE"
STEP_NAME = "UNIT_TEST_STEP"

logging.disable(logging.CRITICAL)


class MockHttpResponse(object):  # pylint: disable=too-few-public-methods
    """Mock response for Energy recorder API."""

    def __init__(self, text, status_code):
        """Create an instance of MockHttpResponse."""
        self.text = text
        self.status_code = status_code


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


class EnergyRecorderTest(unittest.TestCase):
    """Energy module unitary test suite."""

    case_name = CASE_NAME
    request_headers = {'content-type': 'application/json'}

    @mock.patch('functest.energy.energy.requests.post',
                return_value=RECORDER_OK)
    def testtest_start(self, post_mock=None):
        """EnergyRecorder.start method (regular case)."""
        self.assertTrue(EnergyRecorder.start(self.case_name))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers
        )

    @mock.patch('functest.energy.energy.requests.post',
                side_effect=Exception("Internal execution error (MOCK)"))
    def testtest_start_error(self, post_mock=None):
        """EnergyRecorder.start method (error in method)."""
        self.assertFalse(EnergyRecorder.start(self.case_name))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers
        )

    @mock.patch('functest.energy.energy.requests.post',
                return_value=RECORDER_KO)
    def testtest_start_api_error(self, post_mock=None):
        """EnergyRecorder.start method (API error)."""
        self.assertFalse(EnergyRecorder.start(self.case_name))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers
        )

    @mock.patch('functest.energy.energy.requests.post',
                return_value=RECORDER_OK)
    def testtest_set_step(self, post_mock=None):
        """EnergyRecorder.set_step method (regular case)."""
        self.assertTrue(EnergyRecorder.set_step(STEP_NAME))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"] + "/step",
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers
        )

    @mock.patch('functest.energy.energy.requests.post',
                return_value=RECORDER_KO)
    def testtest_set_step_api_error(self, post_mock=None):
        """EnergyRecorder.set_step method (API error)."""
        self.assertFalse(EnergyRecorder.set_step(STEP_NAME))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"] + "/step",
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers
        )

    @mock.patch('functest.energy.energy.requests.post',
                side_effect=Exception("Internal execution error (MOCK)"))
    def testtest_set_step_error(self, post_mock=None):
        """EnergyRecorder.set_step method (method error)."""
        self.assertFalse(EnergyRecorder.set_step(STEP_NAME))
        post_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"] + "/step",
            auth=EnergyRecorder.energy_recorder_api["auth"],
            data=mock.ANY,
            headers=self.request_headers
        )

    @mock.patch('functest.energy.energy.requests.delete',
                return_value=RECORDER_OK)
    def testtest_stop(self, delete_mock=None):
        """EnergyRecorder.stop method (regular case)."""
        self.assertTrue(EnergyRecorder.stop())
        delete_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            headers=self.request_headers
        )

    @mock.patch('functest.energy.energy.requests.delete',
                return_value=RECORDER_KO)
    def testtest_stop_api_error(self, delete_mock=None):
        """EnergyRecorder.stop method (API Error)."""
        self.assertFalse(EnergyRecorder.stop())
        delete_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            headers=self.request_headers
        )

    @mock.patch('functest.energy.energy.requests.delete',
                side_effect=Exception("Internal execution error (MOCK)"))
    def testtest_stop_error(self, delete_mock=None):
        """EnergyRecorder.stop method (method error)."""
        self.assertFalse(EnergyRecorder.stop())
        delete_mock.assert_called_once_with(
            EnergyRecorder.energy_recorder_api["uri"],
            auth=EnergyRecorder.energy_recorder_api["auth"],
            headers=self.request_headers
        )

    @energy.set_step(STEP_NAME)
    def do_some_stuff(self):
        """Fake method to test energy.test_step decorator."""
        pass

    @energy.enable_recording
    def decorated_method(self):
        """Call with to energy recorder decorators."""
        self.do_some_stuff()

    @mock.patch('functest.energy.energy.EnergyRecorder')
    def test_decorators(self, recorder_mock):
        """Test energy module decorators."""
        self.decorated_method()
        calls = [mock.call.start(self.case_name),
                 mock.call.set_step(STEP_NAME),
                 mock.call.stop()]
        recorder_mock.assert_has_calls(calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
