#!/usr/bin/env python

# pylint: disable=missing-docstring

import errno
import os
import urlparse

import mock
import requests.sessions


def can_dump_request_to_file(method):

    def dump_preparedrequest(request, **kwargs):
        # pylint: disable=unused-argument
        parseresult = urlparse.urlparse(request.url)
        if parseresult.scheme == "file":
            try:
                dirname = os.path.dirname(parseresult.path)
                os.makedirs(dirname)
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    raise
            with open(parseresult.path, 'a') as dumpfile:
                headers = ""
                for key in request.headers:
                    headers += key + " " + request.headers[key] + "\n"
                message = "{} {}\n{}\n{}\n\n\n".format(
                    request.method, request.url, headers, request.body)
                dumpfile.write(message)
        return mock.Mock()

    def patch_request(method, url, **kwargs):
        with requests.sessions.Session() as session:
            parseresult = urlparse.urlparse(url)
            if parseresult.scheme == "file":
                with mock.patch.object(session, 'send',
                                       side_effect=dump_preparedrequest):
                    return session.request(method=method, url=url, **kwargs)
            else:
                return session.request(method=method, url=url, **kwargs)

    def hook(*args, **kwargs):
        with mock.patch('requests.api.request', side_effect=patch_request):
            return method(*args, **kwargs)

    return hook
