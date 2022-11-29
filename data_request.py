#!/usr/bin/python3

# On importe les librairies nécessaires
import json
import requests
from typing import Any

# On crée la classe de dataRequest


class DataRequest:
    """
    This class allows to make request to the API

    :author: Panda <panda@delmasweb.net>
    :date: 30 Août 2021
    :version: 1.0
"""

    def __init__(self, api_key: str) -> None:
        """
                Constructor

                :param api_key: API Key
                :type api_key: str
        """
        self.__setApiKey(api_key)

    def __setApiKey(self, api_key: str) -> None:
        """
                API Key setter

                :param api_key: API Key
                :type api_key: str
                :meta private:
        """
        self.__api_key = api_key

    def __getApiKey(self) -> str:
        """
                API Key getter

                :returns: API's key
                :rtype: str
                :meta private:
        """
        return self.__api_key

    def __makeRequest(self, uri: str, url: str, getParams: str = None, payload: str = None, methodHTTP: str = "GET") -> Any:
        """
                This method do the HTTP REST API calls

                :param uri: Website URI
                :type uri: str
                :param url: Access route on the server
                :type url: str
                :param getParams: GET parameters
                :type getParams: str
                :param payload: A JSON serialized object (see json.dumps)
                :type payload: str
                :param methodHTTP: HTTP Method (i.e GET or POST)
                :type methodHTTP: str
                :raise Exception: An exception if the result of the request is >= 400
                :meta private:
        """
        url = uri+"/"+url

        if(getParams):
            url = url + "?"+getParams

        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}
                   
        if self.__getApiKey() is not None:
            headers['api_key'] = self.__getApiKey()
        
        response = None

        try:
            if methodHTTP == "GET":
                response = requests.get(url)
            elif methodHTTP == "POST":
                response = requests.post(url, data=payload, headers=headers)

            if response != None:
                data = response.json()
                data["status"] = response.status_code
                return data
            else:
                raise Exception("No reponse")
        except Exception as e:
            raise Exception(
                "Request cannot be made. Connection cannot be set. Max retries failed")

    def __createConnectionPayload(self, params: dict) -> str:
        """
                This method creates the payload from a given dictionnary if needed

                :param params: The dictionnary that will be transformed in JSON result
                :type params: dict
                :meta private:
        """
        return json.dumps(params)

    def makeRequest(self, uri: str, url: str, getParams: str = None, params: dict = {}, methodHTTP: str = "GET") -> Any:
        """
                This request is the exposed part to make the request

                :param uri: API's URI
                :type uri: str
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
        try:
            payload = self.__createConnectionPayload(params)
            return self.__makeRequest(uri=uri, url=url, getParams=getParams, payload=payload, methodHTTP=methodHTTP)
        except Exception as e:
            raise e
