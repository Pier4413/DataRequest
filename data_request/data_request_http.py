# On importe les librairies nécessaires
import json
import requests
from enum import Enum
from typing import Any, Optional

from .data_request import DataRequest

class HTTPMethod(Enum):
  GET = "GET",
  POST = "POST"

class DataRequestHTTP(DataRequest):
  """
  This class allows to make request to the API

  :author: Panda <panda@delmasweb.net>
  :date: 2021-08-30
  :version: 1.0
  """

  def __init__(self, api_key: str, uri: str) -> None:
    """
      Constructor

      :param api_key: API Key
      :type api_key: str
      :param uri: Website URI
      :type uri: str
    """
    self.api_key = api_key
    self.uri = uri

  def __makeRequest(self,
                    url: str,
                    get_params: Optional[str] = None,
                    payload: Optional[str] = None,
                    http_method: HTTPMethod = HTTPMethod.GET) -> Any:
    """
      This method do the HTTP REST API calls

      :param url: Access route on the server
      :type url: str
      :param get_params: GET parameters
      :type get_params: str
      :param payload: A JSON serialized object (see json.dumps)
      :type payload: str
      :param HTTP_method: HTTP Method (i.e GET or POST)
      :type HTTP_method: str
      :raise Exception: An exception if the result of the request is >= 400
      :meta private:
    """
    url = self.uri+"/"+url

    if (get_params):
      url = url + "?"+get_params

    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}

    if self.api_key is not None:
      headers['Api-Key'] = self.api_key

    response = None

    try:

      match http_method:
        case HTTPMethod.GET:
          response = requests.get(url, headers=headers)
        case HTTPMethod.POST:
          response = requests.post(url, data=payload, headers=headers)

      if response != None:
        data = response.json()
        data["status"] = response.status_code
        return data
      else:
        raise Exception("No reponse")
    except Exception as e:
      raise Exception(
          f"Request cannot be made. Connection cannot be set. Exception is {e}")

  def __createConnectionPayload(self, params: dict) -> str:
    """
      This method creates the payload from a given dictionnary if needed

      :param params: The dictionnary that will be transformed in JSON result
      :type params: dict
      :meta private:
    """
    return json.dumps(params)

  def makeRequest(self,
                  url: str,
                  get_params: Optional[str] = None,
                  params: dict = {},
                  http_method: HTTPMethod = HTTPMethod.GET) -> Any:
    """
      This request is the exposed part to make the request

      :param url: API's route
      :type url: str
      :param get_params: Optional; Default : None; The GET parameters if needed
      :type get_params: str
      :param params: Optional; Default: {}; A payload in a dictionnary format
      :type params: dict
      :param http_method: Optional; Default : GET; The HTTP method (i.e GET or POST)
      :type http_method: str
      :returns: The request result as a dictionnary
      :raise: An exception in case of failure
      :rtype: Any
      :meta public:
    """
    try:
      payload = self.__createConnectionPayload(params)
      return self.__makeRequest(url, get_params, payload, http_method)
    except Exception as e:
      raise e
