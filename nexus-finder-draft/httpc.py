
import urllib.request
import urllib.error
import base64
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

import json

from pathlib import Path

from typing import Union

StrPath = Union[str, Path]

import logging

logger = logging.getLogger().getChild('http')


class HTTPError(Exception):
    """Error fetching resource"""


def _requestfactory(url: str, auth: tuple, params: dict=None):
    if params:
        url_values = urllib.parse.urlencode(params)
        # data = params.encode('ascii')
        url += '?' + url_values
        logger.debug('Requesting: %s' % url)
    login, password = auth
    req = urllib.request.Request(url)
    if login and password:
        base64string = base64.b64encode(bytes('%s:%s' % (login, password), 'ascii')).decode()
        req.add_header("Authorization", "Basic %s" % base64string)
    return req


def fetchfile(url: str, *, destfilepath: StrPath, auth: tuple, params: dict=None):
    if isinstance(destfilepath, Path):
        destfilepath = str(destfilepath.resolve())
    try:
        req = _requestfactory(url, auth, params)

        # fpath, _httpmessage = request.urlretrieve(request, destfilepath)

        with urllib.request.urlopen(req) as response, open(destfilepath, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        return destfilepath
    except urllib.error.URLError as ex:
        logger.error(str(ex))
        raise HTTPError from ex
    except urllib.error.HTTPError as ex:
        logger.error(str(ex))
        raise HTTPError from ex


def getjson(url: str, *, auth: tuple, params: dict=None, timeout: float=15.) -> dict:
    try:
        req = _requestfactory(url, auth, params)

        r = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.URLError as ex:
        logger.error(str(ex))
        raise HTTPError from ex
    except urllib.error.HTTPError as ex:
        logger.error(str(ex))
        raise HTTPError from ex
    # data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    data = json.load(r)
    logger.debug('Response: %s %s' % (r.getcode(), json.dumps(data)))
    # return dict(**data)
    return data
