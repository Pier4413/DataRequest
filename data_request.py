#!/usr/bin/python3

# On importe les librairies nécessaires
from typing import Any

# On crée la classe de dataRequest
class DataRequest(object):
    """
      This class allows to make request. It's a meta class from all data request handlers

      :author: Panda <panda@delmasweb.net>
      :date: 30 Août 2021
      :version: 2.0
    """
    def __init__(self) -> None:
        """
          Constructor
        """

    def makeRequest(self) -> Any:
        """
                This request is the exposed part to make the request

                :param url: API's route
                :type url: str
                :param getParams: Optional; Default : ""; The GET parameters if needed
                :type getParams: str
                :param params: Optional; Default: {}; A payload in a dictionnary format
                :type params: dict
                :param methodHTTP: Optional; Default : GET; The HTTP method (i.e GET or POST)
                :type methodHTTP: str
                :returns: The request result as a dictionnary
                :raise: An exception in case of failure
                :rtype: Any
                :meta public:
        """
        raise NotImplementedError
