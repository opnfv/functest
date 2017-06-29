#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from functest.api.base import ApiResource


class Envs(ApiResource):
    def get(self):
        return self._dispatch_get()


# class EnvsAction(ApiResource):
#     def post(self):
#         return self._dispatch_post()


class OpenStackCredentials(ApiResource):
    def get(self):
        return self._dispatch_get()


# class OpenStackAction(ApiResource):
#     def post(self):
#         return self._dispatch_post()


class Testcases(ApiResource):
    def get(self):
        return self._dispatch_get()


# class TestcasesOne(ApiResource):
#     def get(self):
#         return self._dispatch_get()


# class TestcasesAction(ApiResource):
#     def post(self):
#         return self._dispatch_post()


class Tiers(ApiResource):
    def get(self):
        return self._dispatch_get()


# class TiersOne(ApiResource):
#     def get(self):
#         return self._dispatch_get()


# class TestcasesinOneTier(ApiResource):
#     def get(self):
#         return self._dispatch_get()


# class TiersAction(ApiResource):
#     def post(self):
#         return self._dispatch_post()


# class Tasks(ApiResource):
#     def get(self):
#         return self._dispatch_get()
