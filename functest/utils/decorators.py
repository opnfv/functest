#!/usr/bin/env python

import mock
import requests.sessions
import urlparse


def can_dump_request_to_file(method):

    def dump_preparedrequest(request, **kwargs):
        parseresult = urlparse.urlparse(request.url)
        if parseresult.scheme == "file":
            filepath = parseresult.path[0:parseresult.path.rfind('/results')]
            fileurl = "file://" + filepath
            with open(filepath, 'a') as f:
                headers = ""
                for key in request.headers:
                    headers += key + " " + request.headers[key] + "\n"
                message = "{} {}\n{}\n{}\n\n\n".format(
                    request.method, fileurl, headers, request.body)
                f.write(message)
        return mock.Mock()

    def patch_request(method, url, **kwargs):
        with requests.sessions.Session() as session:
            parseresult = urlparse.urlparse(url)
            if parseresult.scheme == "file":
                with mock.patch.object(
                        session, 'send', side_effect=dump_preparedrequest):
                    return session.request(method=method, url=url, **kwargs)
            else:
                return session.request(method=method, url=url, **kwargs)

    def hook(*args, **kwargs):
        with mock.patch('requests.api.request', side_effect=patch_request):
            return method(*args, **kwargs)

    return hook
