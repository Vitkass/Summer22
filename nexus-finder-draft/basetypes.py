from typing import Union, Any, Mapping, List

import urllib.parse
import urllib
import json

import httpc

from pathlib import Path

StrPath = Union[str, Path]


# Type of packages - classified by element names in release.xml
class Packtype:
    EXCEPTION = 'ExceptionPackage'
    ACTION = 'ImpPackage'
    CONVERTER = 'ConverterPackage'
    ENGINE = 'EnginePackage'
    DEPENDENCY_INTERNAL = 'internal'
    DEPENDENCY_EXTERNAL = 'external'



class NexusStorage:

    def __init__(self, *, 
            nexus_host: str, 
            nexus_user: str, 
            nexus_pwd: str) -> None:

        # nexus_pwd = urllib.parse.quote_plus(nexus_pwd)
        self.url = '{nexus_host}/service/rest/v1/'.format(
            nexus_host=nexus_host)
        self.host = nexus_host.split('//')[-1]
        self.auth = (nexus_user, nexus_pwd)


    def search(self, *, repo: str, group: str, package:str, version: str, meta: dict=None) -> dict:
        # search API: https://help.sonatype.com/repomanager3/integrations/rest-and-integration-api/search-api
        meta = meta or {}
        kargs = dict(
            repository=repo,
            group=group,
            version=version,
            **meta
        )
        # Encode arguments, drop "empty" values:
        args = {k: v for k, v in kargs.items() if bool(v)}
        path = 'search/assets'
        url = self.url + path
        response = httpc.getjson(url, auth=self.auth, params=args)
        items = response.get('items', [])
        # ?<query>&continuationToken=88491cd1d185dd136f143f20c4e7d50c

        continuationtoken = response.get('continuationToken')

        while continuationtoken is not None:
            nextargs = {'continuationToken': continuationtoken, **args}
            response = httpc.getjson(url, auth=self.auth, params=nextargs)
            items += response.get('items', [])
            continuationtoken = response.get('continuationToken')
    
        return items


    def listrepos(self):
        # /service/rest/v1/repositories
        path = 'repositories'
        url = self.url + path
        response = httpc.getjson(url, auth=self.auth)
        return response

    
#     def fetchto(self, *, 
#             dist: Distro,
#             group: str, 
#             package: str, 
#             version: str,
#             filter_ext: List[str] = None,
#             filter_repos: List[str] = None):

#         found = []
#         for repo in repos:
#             try:
#                 res = self.search()
#             except:
#                 pass

#         # dist.dir_for(resname)



# class Distro:

#     def __init__(self, rootdir: StrPath) -> None:
#         self.rootdir = rootdir

#     def fetch(self, *,
#             nexus: NexusStorage,
#             package: str, 
#             version: str,
#             group: str=None, 
#             filter_ext: List[str] = None,
#             filter_repos: List[str] = None):
#         pass


if __name__ == '__main__': 

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
