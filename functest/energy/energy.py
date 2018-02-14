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
import traceback

from functools import wraps
import requests
from six.moves import urllib

from functest.utils import env


def finish_session(current_scenario):
    """Finish a recording session."""
    if current_scenario is None:
        EnergyRecorder.stop()
    else:
        EnergyRecorder.logger.debug("Restoring previous scenario (%s/%s)",
                                    current_scenario["scenario"],
                                    current_scenario["step"])
        EnergyRecorder.submit_scenario(
            current_scenario["scenario"],
            current_scenario["step"]
        )


def enable_recording(method):
    """
    Record energy during method execution.

    Decorator to record energy during "method" exection.

        param method: Method to suround with start and stop
        :type method: function

        .. note:: "method" should belong to a class having a "case_name"
                  attribute
    """
    @wraps(method)
    def wrapper(*args):
        """
        Record energy during method execution (implementation).

        Wrapper for decorator to handle method arguments.
        """
        current_scenario = EnergyRecorder.get_current_scenario()
        EnergyRecorder.start(args[0].case_name)
        try:
            return_value = method(*args)
            finish_session(current_scenario)
        except Exception as exc:  # pylint: disable=broad-except
            EnergyRecorder.logger.exception(exc)
            finish_session(current_scenario)
            raise exc
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

    # Default connection timeout
    CONNECTION_TIMEOUT = 4

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
            assert env.get('NODE_NAME')
            assert env.get('ENERGY_RECORDER_API_URL')
            environment = env.get('NODE_NAME')
            energy_recorder_uri = env.get(
                'ENERGY_RECORDER_API_URL')

            # Creds
            creds_usr = env.get("ENERGY_RECORDER_API_USER")
            creds_pass = env.get("ENERGY_RECORDER_API_PASSWORD")

            uri_comp = "/recorders/environment/"
            uri_comp += urllib.parse.quote_plus(environment)

            if creds_usr != "" and creds_pass != "":
                energy_recorder_api_auth = (creds_usr, creds_pass)
            else:
                energy_recorder_api_auth = None

            try:
                resp = requests.get(energy_recorder_uri + "/monitoring/ping",
                                    auth=energy_recorder_api_auth,
                                    headers={
                                        'content-type': 'application/json'
                                    },
                                    timeout=EnergyRecorder.CONNECTION_TIMEOUT)
                api_available = json.loads(resp.text)["status"] == "OK"
                EnergyRecorder.logger.info(
                    "API recorder available at : %s",
                    energy_recorder_uri + uri_comp)
            except Exception as exc:  # pylint: disable=broad-except
                EnergyRecorder.logger.info(
                    "Energy recorder API is not available, cause=%s",
                    str(exc))
                api_available = False
            # Final config
            EnergyRecorder.energy_recorder_api = {
                "uri": energy_recorder_uri + uri_comp,
                "auth": energy_recorder_api_auth,
                "available": api_available
            }
        return EnergyRecorder.energy_recorder_api["available"]

    @staticmethod
    def submit_scenario(scenario, step):
        """
        Submit a complet scenario definition to Energy recorder API.

            param scenario: Scenario name
            :type scenario: string
            param step: Step name
            :type step: string
        """
        try:
            return_status = True
            # Ensure that connectyvity settings are loaded
            if EnergyRecorder.load_config():
                EnergyRecorder.logger.debug("Submitting scenario (%s/%s)",
                                            scenario, step)

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
                    },
                    timeout=EnergyRecorder.CONNECTION_TIMEOUT
                )
                if response.status_code != 200:
                    EnergyRecorder.logger.error(
                        "Error while submitting scenario\n%s",
                        response.text)
                    return_status = False
        except requests.exceptions.ConnectionError:
            EnergyRecorder.logger.warning(
                "submit_scenario: Unable to connect energy recorder API")
            return_status = False
        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.info(
                "Error while submitting scenarion to energy recorder API\n%s",
                traceback.format_exc()
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
            if EnergyRecorder.load_config():
                EnergyRecorder.logger.debug("Starting recording")
                return_status = EnergyRecorder.submit_scenario(
                    scenario,
                    EnergyRecorder.INITIAL_STEP
                )

        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.info(
                "Error while starting energy recorder API\n%s",
                traceback.format_exc()
            )
            return_status = False
        return return_status

    @staticmethod
    def stop():
        """Stop current recording session."""
        return_status = True
        try:
            # Ensure that connectyvity settings are loaded
            if EnergyRecorder.load_config():
                EnergyRecorder.logger.debug("Stopping recording")

                # Call API to stop energy recording
                response = requests.delete(
                    EnergyRecorder.energy_recorder_api["uri"],
                    auth=EnergyRecorder.energy_recorder_api["auth"],
                    headers={
                        'content-type': 'application/json'
                    },
                    timeout=EnergyRecorder.CONNECTION_TIMEOUT
                )
                if response.status_code != 200:
                    EnergyRecorder.logger.error(
                        "Error while stating energy recording session\n%s",
                        response.text)
                    return_status = False
        except requests.exceptions.ConnectionError:
            EnergyRecorder.logger.warning(
                "stop: Unable to connect energy recorder API")
            return_status = False
        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.info(
                "Error while stoping energy recorder API\n%s",
                traceback.format_exc()
            )
            return_status = False
        return return_status

    @staticmethod
    def set_step(step):
        """Notify energy recording service of current step of the testcase."""
        return_status = True
        try:
            # Ensure that connectyvity settings are loaded
            if EnergyRecorder.load_config():
                EnergyRecorder.logger.debug("Setting step")

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
                    },
                    timeout=EnergyRecorder.CONNECTION_TIMEOUT
                )
                if response.status_code != 200:
                    EnergyRecorder.logger.error(
                        "Error while setting current step of testcase\n%s",
                        response.text)
                    return_status = False
        except requests.exceptions.ConnectionError:
            EnergyRecorder.logger.warning(
                "set_step: Unable to connect energy recorder API")
            return_status = False
        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.info(
                "Error while setting step on energy recorder API\n%s",
                traceback.format_exc()
            )
            return_status = False
        return return_status

    @staticmethod
    def get_current_scenario():
        """Get current running scenario (if any, None else)."""
        return_value = None
        try:
            # Ensure that connectyvity settings are loaded
            if EnergyRecorder.load_config():
                EnergyRecorder.logger.debug("Getting current scenario")

                # Call API get running scenario
                response = requests.get(
                    EnergyRecorder.energy_recorder_api["uri"],
                    auth=EnergyRecorder.energy_recorder_api["auth"],
                    timeout=EnergyRecorder.CONNECTION_TIMEOUT
                )
                if response.status_code == 200:
                    return_value = json.loads(response.text)
                elif response.status_code == 404:
                    EnergyRecorder.logger.info(
                        "No current running scenario at %s",
                        EnergyRecorder.energy_recorder_api["uri"])
                    return_value = None
                else:
                    EnergyRecorder.logger.error(
                        "Error while getting current scenario\n%s",
                        response.text)
                    return_value = None
        except requests.exceptions.ConnectionError:
            EnergyRecorder.logger.warning(
                "get_currernt_sceario: Unable to connect energy recorder API")
            return_value = None
        except Exception:  # pylint: disable=broad-except
            # Default exception handler to ensure that method
            # is safe for caller
            EnergyRecorder.logger.info(
                "Error while getting current scenario from energy recorder API"
                "\n%s", traceback.format_exc()
            )
            return_value = None
        return return_value
