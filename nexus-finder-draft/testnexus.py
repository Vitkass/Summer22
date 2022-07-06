from basetypes import NexusStorage
from confloader import loadconf

import json

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    handlers=[
        logging.StreamHandler() # if args.verbose else logging.NullHandler()
    ]
)
logger = logging.getLogger()

conf = loadconf()

nexus_host = conf.nexus_host
nexus_user = conf.nexus_usr
nexus_pwd = conf.nexus_pwd

nexus = NexusStorage(nexus_host=nexus_host, nexus_user=nexus_user, nexus_pwd=nexus_pwd)

# res = nexus.listrepos()

# print(res)


res = nexus.search(repo='pypi-local', group='', package='Robin.*', version=''
    , meta={'pypi.name': 'poppler'}
    )
# res = nexus.search(repo='maven-local', group='', package='Robin.*', version='')

print(json.dumps(res))

