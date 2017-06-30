#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""This module manages calls to Energy recording API."""

import json
import logging
import urllib
import requests

import functest.utils.functest_utils as ft_utils


def enable_recording(method):
    """
    Record energy during method execution.

    Decorator to record energy during "method" exection.

        param method: Method to suround with start and stop
        :type method: function

        .. note:: "method" should belong to a class having a "case_name"
                  attribute
    """
    def wrapper(*args):
        """
        Record energy during method execution (implementation).

        Wrapper for decorator to handle method arguments.
        """
        current_scenario = EnergyRecorder.get_current_scenario()
        EnergyRecorder.start(args[0].case_name)
        return_value = method(*args)
        if current_scenario is None:
            EnergyRecorder.stop()
        else:
            EnergyRecorder.submit_scenario(
                current_scenario["scenario"],
                current_scenario["step"]
            )
        return return_value
    return wrapper


# Class to manage energy recording sessions
class EnergyRecorder(object):
    """Manage Energy recording session."""

    logger = logging.getLogger(__name__)
    # Energy recording API connectivity settings
    # see load_config method
    energy_recorder_api = None

    # Default initial step
    INITIAL_STEP = "running"

    @staticmethod
    def load_config():
        """
        Load connectivity settings from yaml.

        Load connectivity settings to Energy recording API
        Use functest global config yaml file
        (see functest_utils.get_functest_config)
        """
        # Singleton pattern for energy_recorder_api static member
        # Load only if not previouly done
        if EnergyRecorder.energy_recorder_api is None:
            environment = ft_utils.get_pod_name()

            # API URL
            energy_recorder_uri = ft_utils.get_functest_config(
                "energy_recorder.api_url")
            assert energy_recorder_uri
            assert environment

            energy_recorder_uri += "/recorders/environment/"
            energy_recorder_uri += urllib.quote_plus(environment)
            EnergyRecorder.logger.debug(
                "API recorder at: " + energy_recorder_uri)

            # Creds
            user = ft_utils.get_functest_config(
                "energy_recorder.api_user")
            password = ft_utils.get_functest_config(
                "energy_recorder.api_password")

            if user != "" and password != "":
                energy_recorder_api_auth = (user, password)
            else:
                energy_recorder_api_auth = None

            # Final config
            EnergyRecorder.energy_recorder_api = {
                "uri": energy_recorder_uri,
                "auth": energy_recorder_api_auth
            }

    @staticmethod
    def submit_scenario(scenario, step):
        """
        Submit a complet scenario definition to Energy recorder API.

            param scenario: Scenario name
            :type scenario: string
            param step: Step name
            :type step: string
        """
        return_status = True
        try:
            EnergyRecorder.logger.debug("Submitting scenario")
            # Ensure that connectyvity settings are loaded
            EnergyRecorder.load_config()

            # Create API payload
            payload = {
                "step": step,
                "scenario": scenario
            }
            # Call API to start energy recording
            response = requests.post(
                EnergyRecorder.energy_recorder_api["uri"],
                data=json.dumps(payload),
                auth=EnergyRecorder.energy_recorder_api["auth"],
                headers={
                    'content-type': 'application/json'
                }
            )
            if response.status_code != 200:
                log_msg = "Error while submitting scenario\n{}"
                log_msg = log_msg.format(response.text)
                EnergyRecorder.logger.info(log_msg)
                return_status = False
        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.exception(
                "Error while submitting scenarion to energy recorder API"
            )
            return_status = False
        return return_status

    @staticmethod
    def start(scenario):
        """
        Start a recording session for scenario.

            param scenario: Starting scenario
            :type scenario: string
        """
        return_status = True
        try:
            EnergyRecorder.logger.debug("Starting recording")
            return_status = EnergyRecorder.submit_scenario(
                scenario,
                EnergyRecorder.INITIAL_STEP
            )

        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.exception(
                "Error while starting energy recorder API"
            )
            return_status = False
        return return_status

    @staticmethod
    def stop():
        """Stop current recording session."""
        EnergyRecorder.logger.debug("Stopping recording")
        return_status = True
        try:
            # Ensure that connectyvity settings are loaded
            EnergyRecorder.load_config()

            # Call API to stop energy recording
            response = requests.delete(
                EnergyRecorder.energy_recorder_api["uri"],
                auth=EnergyRecorder.energy_recorder_api["auth"],
                headers={
                    'content-type': 'application/json'
                }
            )
            if response.status_code != 200:
                log_msg = "Error while stating energy recording session\n{}"
                log_msg = log_msg.format(response.text)
                EnergyRecorder.logger.error(log_msg)
                return_status = False
        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.exception(
                "Error while stoping energy recorder API"
            )
            return_status = False
        return return_status

    @staticmethod
    def set_step(step):
        """Notify energy recording service of current step of the testcase."""
        EnergyRecorder.logger.debug("Setting step")
        return_status = True
        try:
            # Ensure that connectyvity settings are loaded
            EnergyRecorder.load_config()

            # Create API payload
            payload = {
                "step": step,
            }

            # Call API to define step
            response = requests.post(
                EnergyRecorder.energy_recorder_api["uri"] + "/step",
                data=json.dumps(payload),
                auth=EnergyRecorder.energy_recorder_api["auth"],
                headers={
                    'content-type': 'application/json'
                }
            )
            if response.status_code != 200:
                log_msg = "Error while setting current step of testcase\n{}"
                log_msg = log_msg.format(response.text)
                EnergyRecorder.logger.error(log_msg)
                return_status = False
        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.exception(
                "Error while setting step on energy recorder API"
            )
            return_status = False
        return return_status

    @staticmethod
    def get_current_scenario():
        """Get current running scenario (if any, None else)."""
        EnergyRecorder.logger.debug("Getting current scenario")
        return_value = None
        print "In get current"
        try:
            # Ensure that connectyvity settings are loaded
            EnergyRecorder.load_config()

            # Call API get running scenario
            response = requests.get(
                EnergyRecorder.energy_recorder_api["uri"],
                auth=EnergyRecorder.energy_recorder_api["auth"]
            )
            if response.status_code == 200:
                return_value = json.loads(response.text)
            elif response.status_code == 404:
                log_msg = "No current running scenario at {}"
                log_msg = log_msg.format(
                    EnergyRecorder.energy_recorder_api["uri"])
                EnergyRecorder.logger.error(log_msg)
                print log_msg
                return_value = None
            else:
                log_msg = "Error while getting current scenario\n{}"
                log_msg = log_msg.format(response.text)
                EnergyRecorder.logger.error(log_msg)
                print log_msg
                return_value = None
        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.exception(
                "Error while getting current scenario from energy recorder API"
            )
            return_value = None
        return return_value
