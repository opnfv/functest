#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock
from tackerclient.v1_0 import client as tackerclient

from functest.utils import openstack_tacker
from functest.tests.unit import test_utils


class OSTackerTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.tacker_client = mock.Mock()
        self.getresponse = {'vnfds': [{'id': 'test_id'}],
                            'vnfs': [{'id': 'test_id'}],
                            'sfcs': [{'id': 'test_id'}]}
        self.vnfdlist = {'vnfds': [{'id': 'test_vnfd1'}, {'id': 'test_vnfd2'}]}
        self.vnflist = {'vnfs': [{'id': 'test_vnf1'}, {'id': 'test_vnf2'}]}
        self.sfclist = {'sfcs': [{'id': 'test_sfc1'}, {'id': 'test_sfc2'}]}
        self.sfc_classifierlist = {'sfc_classifiers': [{'id': 'test_sfc_cl1'},
                                   {'id': 'test_sfc_cl2'}]}

        self.createvnfd = {"vnfd": {"attributes": {"vnfd": 'vnfd_body'}}}
        self.createvnf = {"vnf": {"attributes": {"vnf": 'vnf_body'}}}
        self.createsfc = {"sfc": {"attributes": {"sfc": 'sfc_body'}}}
        self.createsfc_clf = {"sfc_classifier": {"attributes":
                                                 {"sfc_clf": 'sfc_clf_body'}}}

        self.resource_type = 'vnfd'
        self.resource_name = 'resource_name'
        self.tosca_file = 'test_tosca_file'
        self.vnfd = 'test_vnfd'
        self.vnf = 'test_vnf'
        self.sfc = 'test_sfc'
        self.sfc_clf = 'test_sfc_clf'

    def _get_creds(self):
        cred_dict = {
            'OS_USERNAME': 'username',
            'OS_PASSWORD': 'password',
            'OS_AUTH_URL': 'auth_url',
            'OS_TENANT_NAME': 'tenant_name',
            'OS_USER_DOMAIN_NAME': 'user_domain_name',
            'OS_PROJECT_DOMAIN_NAME': 'project_domain_name',
            'OS_PROJECT_NAME': 'project_name',
            'OS_ENDPOINT_TYPE': 'endpoint_type',
            'OS_REGION_NAME': 'region_name'
        }
        return cred_dict

    def test_get_tacker_client(self):
        with mock.patch('functest.utils.openstack_tacker.'
                        'os_utils.get_session'):
            tackerclient.Client = mock.Mock
            ret = openstack_tacker.get_tacker_client()
            self.assertTrue(isinstance(ret, mock.Mock))

    def test_get_id_from_name(self):
        with mock.patch.object(self.tacker_client, 'get',
                               return_value=self.getresponse):
            resp = openstack_tacker.get_id_from_name(self.tacker_client,
                                                     self.resource_type,
                                                     self.resource_name)
            self.assertEqual(resp, 'test_id')

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_get_id_from_name_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'get',
                               side_effect=Exception):
            resp = openstack_tacker.get_id_from_name(self.tacker_client,
                                                     self.resource_type,
                                                     self.resource_name)
            self.assertIsNone(resp)
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("Error [get"
                                                                  "_id_from_"
                                                                  "name(tacker"
                                                                  "_client"
                                                                  ", resource_"
                                                                  "type, "
                                                                  "resource_"
                                                                  "name)]:"))

    @mock.patch('functest.utils.openstack_tacker.get_id_from_name')
    def test_get_vnfd_id(self, mock_get_id_from_name):
        openstack_tacker.get_vnfd_id(self.tacker_client, self.resource_name)
        mock_get_id_from_name.assert_called_once_with(self.tacker_client,
                                                      'vnfd',
                                                      self.resource_name)

    @mock.patch('functest.utils.openstack_tacker.get_id_from_name')
    def test_get_vnf_id(self, mock_get_id_from_name):
        openstack_tacker.get_vnf_id(self.tacker_client, self.resource_name)
        mock_get_id_from_name.assert_called_once_with(self.tacker_client,
                                                      'vnf',
                                                      self.resource_name)

    @mock.patch('functest.utils.openstack_tacker.get_id_from_name')
    def test_get_sfc_id(self, mock_get_id_from_name):
        openstack_tacker.get_sfc_id(self.tacker_client, self.resource_name)
        mock_get_id_from_name.assert_called_once_with(self.tacker_client,
                                                      'sfc',
                                                      self.resource_name)

    @mock.patch('functest.utils.openstack_tacker.get_id_from_name')
    def test_get_sfc_classifier_id(self, mock_get_id_from_name):
        openstack_tacker.get_sfc_classifier_id(self.tacker_client,
                                               self.resource_name)
        mock_get_id_from_name.assert_called_once_with(self.tacker_client,
                                                      'sfc-classifier',
                                                      self.resource_name)

    def test_list_vnfds(self):
        with mock.patch.object(self.tacker_client, 'list_vnfds',
                               return_value=self.vnfdlist):
            resp = openstack_tacker.list_vnfds(self.tacker_client,
                                               verbose=False)
            self.assertEqual(resp, ['test_vnfd1', 'test_vnfd2'])

    def test_list_vnfds_verbose(self):
        with mock.patch.object(self.tacker_client, 'list_vnfds',
                               return_value=self.vnfdlist):
            resp = openstack_tacker.list_vnfds(self.tacker_client,
                                               verbose=True)
            self.assertEqual(resp, self.vnfdlist)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_list_vnfds_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'list_vnfds',
                               side_effect=Exception):
            resp = openstack_tacker.list_vnfds(self.tacker_client,
                                               verbose=False)
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("Error"
                                                                  " [list"
                                                                  "_vnfds("
                                                                  "tacker_"
                                                                  "client)]:"))
            self.assertIsNone(resp)

    def test_create_vnfd_missing_file(self):
        with mock.patch.object(self.tacker_client, 'create_vnfd',
                               return_value=self.createvnfd):
            resp = openstack_tacker.create_vnfd(self.tacker_client,
                                                tosca_file=None)
            self.assertEqual(resp, self.createvnfd)

    def test_create_vnfd_default(self):
        with mock.patch.object(self.tacker_client, 'create_vnfd',
                               return_value=self.createvnfd), \
                mock.patch('__builtin__.open', mock.mock_open(read_data='1')) \
                as m:
            resp = openstack_tacker.create_vnfd(self.tacker_client,
                                                tosca_file=self.tosca_file)
            m.assert_called_once_with(self.tosca_file)
            self.assertEqual(resp, self.createvnfd)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_create_vnfd_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'create_vnfd',
                               side_effect=Exception):
            resp = openstack_tacker.create_vnfd(self.tacker_client,
                                                tosca_file=self.tosca_file)
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("Error"
                                                                  " [create"
                                                                  "_vnfd("
                                                                  "tacker_"
                                                                  "client, "
                                                                  "'%s')]"
                                                                  % self.
                                                                  tosca_file))
            self.assertIsNone(resp)

    def test_delete_vnfd(self):
        with mock.patch('functest.utils.openstack_tacker.get_vnfd_id',
                        return_value=self.vnfd), \
                mock.patch.object(self.tacker_client, 'delete_vnfd',
                                  return_value=self.vnfd):
            resp = openstack_tacker.delete_vnfd(self.tacker_client,
                                                vnfd_id='vnfd_id',
                                                vnfd_name=self.vnfd)
            self.assertEqual(resp, self.vnfd)

    def test_delete_vnfd_missing_vnfd_name(self):
        with mock.patch('functest.utils.openstack_tacker.get_vnfd_id',
                        return_value=self.vnfd), \
                self.assertRaises(Exception) as context:
            resp = openstack_tacker.delete_vnfd(self.tacker_client,
                                                vnfd_id=None,
                                                vnfd_name=None)
            self.assertIsNone(resp)
            msg = 'You need to provide VNFD id or VNFD name'
            self.assertTrue(msg in context)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_delete_vnfd_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_tacker.get_vnfd_id',
                        return_value=self.vnfd), \
                mock.patch.object(self.tacker_client, 'delete_vnfd',
                                  side_effect=Exception):
            resp = openstack_tacker.delete_vnfd(self.tacker_client,
                                                vnfd_id=None,
                                                vnfd_name=None)
            self.assertIsNone(resp)
            self.assertTrue(mock_logger_error.called)

    def test_list_vnfs(self):
        with mock.patch.object(self.tacker_client, 'list_vnfs',
                               return_value=self.vnflist):
            resp = openstack_tacker.list_vnfs(self.tacker_client,
                                              verbose=False)
            self.assertEqual(resp, ['test_vnf1', 'test_vnf2'])

    def test_list_vnfs_verbose(self):
        with mock.patch.object(self.tacker_client, 'list_vnfs',
                               return_value=self.vnflist):
            resp = openstack_tacker.list_vnfs(self.tacker_client,
                                              verbose=True)
            self.assertEqual(resp, self.vnflist)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_list_vnfs_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'list_vnfs',
                               side_effect=Exception):
            resp = openstack_tacker.list_vnfs(self.tacker_client,
                                              verbose=False)
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("Error"
                                                                  " [list"
                                                                  "_vnfs("
                                                                  "tacker_"
                                                                  "client)]:"))
            self.assertIsNone(resp)

    def test_create_vnf_default(self):
        with mock.patch.object(self.tacker_client, 'create_vnf',
                               return_value=self.createvnf), \
                mock.patch('functest.utils.openstack_tacker.get_vnfd_id',
                           return_value=self.vnf):
            resp = openstack_tacker.create_vnf(self.tacker_client,
                                               vnf_name=self.vnf,
                                               vnfd_id='vnfd_id',
                                               vnfd_name=self.vnfd)
            self.assertEqual(resp, self.createvnf)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_create_vnf_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'create_vnf',
                               side_effect=Exception):
            resp = openstack_tacker.create_vnf(self.tacker_client,
                                               vnf_name=self.vnf,
                                               vnfd_id='vnfd_id',
                                               vnfd_name=self.vnfd)
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("error"
                                                                  " [create"
                                                                  "_vnf("
                                                                  "tacker_"
                                                                  "client"))
            self.assertIsNone(resp)

    def test_wait_for_vnf_vnf_retrieval_failed(self):
        with mock.patch('functest.utils.openstack_tacker.get_vnf',
                        return_value=None), \
                self.assertRaises(Exception) as context:
            openstack_tacker.wait_for_vnf(self.tacker_client,
                                          vnf_id='vnf_id',
                                          vnf_name='vnf_name')
            msg = ("Could not retrieve VNF - id='vnf_id', "
                   "name='vnf_name'")
            self.assertTrue(msg in context)
        with mock.patch('functest.utils.openstack_tacker.get_vnf',
                        side_effect=Exception):
            ret = openstack_tacker.wait_for_vnf(self.tacker_client,
                                                vnf_id='vnf_id',
                                                vnf_name='vnf_name')
            self.assertEqual(ret, None)

    def test_wait_for_vnf_vnf_status_error(self):
        vnf = {'id': 'vnf_id',
               'status': 'ERROR'}
        with mock.patch('functest.utils.openstack_tacker.get_vnf',
                        return_value=vnf), \
                self.assertRaises(Exception) as context:
            openstack_tacker.wait_for_vnf(self.tacker_client,
                                          vnf_id='vnf_id',
                                          vnf_name='vnf_name')
            msg = ('Error when booting vnf vnf_id')
            self.assertTrue(msg in context)

    def test_wait_for_vnf_vnf_timeout(self):
        vnf = {'id': 'vnf_id',
               'status': 'PENDING_CREATE'}
        with mock.patch('functest.utils.openstack_tacker.get_vnf',
                        return_value=vnf), \
                self.assertRaises(Exception) as context:
            openstack_tacker.wait_for_vnf(self.tacker_client,
                                          vnf_id='vnf_id',
                                          vnf_name='vnf_name',
                                          timeout=2)
            msg = ('Timeout when booting vnf vnf_id')
            self.assertTrue(msg in context)

    def test_delete_vnf(self):
        with mock.patch('functest.utils.openstack_tacker.get_vnf_id',
                        return_value=self.vnf), \
                mock.patch.object(self.tacker_client, 'delete_vnf',
                                  return_value=self.vnf):
            resp = openstack_tacker.delete_vnf(self.tacker_client,
                                               vnf_id='vnf_id',
                                               vnf_name=self.vnf)
            self.assertEqual(resp, self.vnf)

    def test_delete_vnf_missing_vnf_name(self):
        with self.assertRaises(Exception) as context:
            openstack_tacker.delete_vnf(self.tacker_client,
                                        vnf_id=None,
                                        vnf_name=None)
            msg = 'You need to provide a VNF id or name'
            self.assertTrue(msg in context)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_delete_vnf_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_tacker.get_vnf_id',
                        return_value=self.vnf), \
                mock.patch.object(self.tacker_client, 'delete_vnf',
                                  side_effect=Exception):
            resp = openstack_tacker.delete_vnf(self.tacker_client,
                                               vnf_id=None,
                                               vnf_name=None)
            self.assertIsNone(resp)
            self.assertTrue(mock_logger_error.called)

    def test_list_sfcs(self):
        with mock.patch.object(self.tacker_client, 'list_sfcs',
                               return_value=self.sfclist):
            resp = openstack_tacker.list_sfcs(self.tacker_client,
                                              verbose=False)
            self.assertEqual(resp, ['test_sfc1', 'test_sfc2'])

    def test_list_sfcs_verbose(self):
        with mock.patch.object(self.tacker_client, 'list_sfcs',
                               return_value=self.sfclist):
            resp = openstack_tacker.list_sfcs(self.tacker_client,
                                              verbose=True)
            self.assertEqual(resp, self.sfclist)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_list_sfcs_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'list_sfcs',
                               side_effect=Exception):
            resp = openstack_tacker.list_sfcs(self.tacker_client,
                                              verbose=False)
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("Error"
                                                                  " [list"
                                                                  "_sfcs("
                                                                  "tacker_"
                                                                  "client)]:"))
            self.assertIsNone(resp)

    def test_create_sfc_default(self):
        with mock.patch.object(self.tacker_client, 'create_sfc',
                               return_value=self.createsfc), \
                mock.patch('functest.utils.openstack_tacker.get_vnf_id',
                           return_value=self.vnf):
            resp = openstack_tacker.create_sfc(self.tacker_client,
                                               sfc_name=self.sfc,
                                               chain_vnf_ids=['chain_vnf_id'],
                                               chain_vnf_names=[self.vnf])
            self.assertEqual(resp, self.createsfc)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_create_sfc_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'create_sfc',
                               side_effect=Exception):
            resp = openstack_tacker.create_sfc(self.tacker_client,
                                               sfc_name=self.sfc,
                                               chain_vnf_ids=['chain_vnf_id'],
                                               chain_vnf_names=[self.vnf])
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("error"
                                                                  " [create"
                                                                  "_sfc("
                                                                  "tacker_"
                                                                  "client"))
            self.assertIsNone(resp)

    def test_delete_sfc(self):
        with mock.patch('functest.utils.openstack_tacker.get_sfc_id',
                        return_value=self.sfc), \
                mock.patch.object(self.tacker_client, 'delete_sfc',
                                  return_value=self.sfc):
            resp = openstack_tacker.delete_sfc(self.tacker_client,
                                               sfc_id='sfc_id',
                                               sfc_name=self.sfc)
            self.assertEqual(resp, self.sfc)

    def test_delete_sfc_missing_sfc_name(self):
        with self.assertRaises(Exception) as context:
            openstack_tacker.delete_sfc(self.tacker_client,
                                        sfc_id=None,
                                        sfc_name=None)
            msg = 'You need to provide an SFC id or name'
            self.assertTrue(msg in context)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_delete_sfc_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_tacker.get_sfc_id',
                        return_value=self.sfc), \
                mock.patch.object(self.tacker_client, 'delete_sfc',
                                  side_effect=Exception):
            resp = openstack_tacker.delete_sfc(self.tacker_client,
                                               sfc_id=None,
                                               sfc_name=None)
            self.assertIsNone(resp)
            self.assertTrue(mock_logger_error.called)

    def test_list_sfc_classifiers(self):
        with mock.patch.object(self.tacker_client, 'list_sfc_classifiers',
                               return_value=self.sfc_classifierlist):
            resp = openstack_tacker.list_sfc_classifiers(self.tacker_client,
                                                         verbose=False)
            self.assertEqual(resp, ['test_sfc_cl1', 'test_sfc_cl2'])

    def test_list_sfc_classifiers_verbose(self):
        with mock.patch.object(self.tacker_client, 'list_sfc_classifiers',
                               return_value=self.sfc_classifierlist):
            resp = openstack_tacker.list_sfc_classifiers(self.tacker_client,
                                                         verbose=True)
            self.assertEqual(resp, self.sfc_classifierlist)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_list_sfc_classifiers_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'list_sfc_classifiers',
                               side_effect=Exception):
            resp = openstack_tacker.list_sfc_classifiers(self.tacker_client,
                                                         verbose=False)
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("Error"
                                                                  " [list"
                                                                  "_sfc_cl"
                                                                  "assifiers("
                                                                  "tacker_"
                                                                  "client)]:"))
            self.assertIsNone(resp)

    def test_create_sfc_classifier_default(self):
        with mock.patch.object(self.tacker_client, 'create_sfc_classifier',
                               return_value=self.createsfc_clf), \
                mock.patch('functest.utils.openstack_tacker.get_sfc_id',
                           return_value=self.sfc):
            cl = self.sfc_clf
            resp = openstack_tacker.create_sfc_classifier(self.tacker_client,
                                                          sfc_clf_name=cl,
                                                          sfc_id='sfc_id',
                                                          sfc_name=self.sfc)
            self.assertEqual(resp, self.createsfc_clf)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_sfc_classifier_exception(self, mock_logger_error):
        with mock.patch.object(self.tacker_client, 'create_sfc_classifier',
                               side_effect=Exception):
            cl = self.sfc_clf
            resp = openstack_tacker.create_sfc_classifier(self.tacker_client,
                                                          sfc_clf_name=cl,
                                                          sfc_id='sfc_id',
                                                          sfc_name=self.sfc)
            mock_logger_error.assert_called_once_with(test_utils.
                                                      SubstrMatch("error"
                                                                  " [create"
                                                                  "_sfc_cl"
                                                                  "assifier("
                                                                  "tacker_"
                                                                  "client"))
            self.assertIsNone(resp)

    def test_delete_sfc_classifier(self):
        with mock.patch('functest.utils.openstack_tacker.get_sfc_'
                        'classifier_id',
                        return_value=self.sfc_clf), \
                mock.patch.object(self.tacker_client, 'delete_sfc_classifier',
                                  return_value=self.sfc_clf):
            cl = self.sfc_clf
            resp = openstack_tacker.delete_sfc_classifier(self.tacker_client,
                                                          sfc_clf_id='sfc_id',
                                                          sfc_clf_name=cl)
            self.assertEqual(resp, cl)

    def test_delete_sfc_classifier_missing_sfc_name(self):
        with self.assertRaises(Exception) as context:
            openstack_tacker.delete_vnf(self.tacker_client,
                                        sfc_clf_id=None,
                                        sfc_clf_name=None)
            msg = 'You need to provide an SFCclassifier id or name'
            self.assertTrue(msg in context)

    @mock.patch('functest.utils.openstack_tacker.logger.error')
    def test_delete_sfc_classifier_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_tacker.get_sfc_'
                        'classifier_id',
                        return_value=self.sfc_clf), \
                mock.patch.object(self.tacker_client, 'delete_sfc_classifier',
                                  side_effect=Exception):
            cl = self.sfc_clf
            resp = openstack_tacker.delete_sfc_classifier(self.tacker_client,
                                                          sfc_clf_id='sfc_id',
                                                          sfc_clf_name=cl)
            self.assertIsNone(resp)
            self.assertTrue(mock_logger_error.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)
