import os

from collections import namedtuple

import logging

logger = logging.getLogger().getChild('loadconf')


Conf = namedtuple('Conf', 'nexus_host nexus_usr nexus_pwd')

def loadconf():
    try:
        with open('.env.robin.dev') as f:
            for line in f:
                name, value = line.strip().split('=')
                value = value.strip('\'\"')
                os.environ[name] = value
                logger.info(f'Adding environment: {name}')
    except Exception as ex:
        logger.warning(f'Cannot load dev environment vars: {ex}')

    nexus_host = os.getenv('NEXUS_HOST')

    nexus_usr = os.getenv('NEXUS_USR')

    nexus_pwd = os.getenv('NEXUS_PWD')

    return Conf(nexus_host, nexus_usr, nexus_pwd)
