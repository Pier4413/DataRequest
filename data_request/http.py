import json
import requests
from enum import Enum
from typing import Optional
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"

class HTTP:
    """
    Classe permettant de faire des requêtes HTTP vers une API avec authentification par clé API.

    :author: Panda <panda@delmasweb.net>
    :date: 2021-08-30
    :version: 1.1
    """

    def __init__(self, api_key: str, host: str, port: str, is_ssl: bool = False, max_retries: int = 1, timeout_ms: int = 500) -> None:
        """
        Initialize the HTTP client.

        :param api_key: API Key for authentication
        :type api_key: str
        :param host: Server hostname
        :type host: str
        :param port: Server port
        :type port: str
        :param is_ssl: True for HTTPS, False for HTTP
        :type is_ssl: bool
        :param max_retries: The maximum number of retries to allow to a connection
        :type max_retries: int
        :param timeout_ms: The timeout in ms to a connection
        :type timeout_ms: int
        """
        protocol = "https" if is_ssl else "http"
        self.api_key = api_key
        self.base_url = f"{protocol}://{host}:{port}"
        self.timeout_ms = timeout_ms

        self.session = requests.Session()

        retries = Retry(
            total=max_retries,
            connect=max_retries,
            read=max_retries,
            status=max_retries,
            allowed_methods=["GET", "HEAD", "POST"],
            status_forcelist=[500, 502, 503, 504],
            backoff_factor=0.0
        )

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount(f"{protocol}://", adapter)

    def __make_request(
        self,
        path: str,
        query_params: Optional[dict] = None,
        payload: Optional[str] = None,
        http_method: HTTPMethod = HTTPMethod.GET
    ) -> dict:
        """
        Do the HTTP request

        :param path: Endpoint path (ex : "/api/status")
        :type path: str
        :param query_params: Parameters to include in the URI
        :type query_params: dict or None
        :param payload: Request body (JSON encodé en chaîne)
        :type payload: str or None
        :param http_method: HTTP Method to use (warning GET doesn't support a body)
        :type http_method: HTTPMethod
        :return: API response with a status code
        :rtype: dict
        :raises Exception: In case of network error or no response
        """
        url = urljoin(self.base_url + "/", path.lstrip("/"))

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Api-Key': self.api_key
        }

        try:
            match http_method:
                case HTTPMethod.GET:
                    response = self.session.get(url, headers=headers, params=query_params, timeout=self.timeout_ms/1000.0)
                case HTTPMethod.POST:
                    response = self.session.post(url, headers=headers, params=query_params, data=payload, timeout=self.timeout_ms/1000.0)
                case _:
                    raise ValueError(f"Méthode HTTP non supportée : {http_method}")

            response.raise_for_status()
            data = response.json()
            data["status"] = response.status_code
            return data

        except Exception as e:
            raise Exception(f"Échec de la requête : {e}")

    def create_payload(self, payload_dict: dict) -> str:
        """
        Parse a dict into a usable JSON for a body

        :param payload_dict: Dict to convert
        :type payload_dict: dict
        :return: JSON representation a string
        :rtype: str
        """
        return json.dumps(payload_dict)

    def make_request(
        self,
        path: str,
        query_params: Optional[dict] = None,
        payload_dict: Optional[dict] = None,
        http_method: HTTPMethod = HTTPMethod.GET
    ) -> dict:
        """
        Send a request to the API with or without a payload.

        :param path: Endpoint path (ex : "/api/status")
        :type path: str
        :param query_params: Parameters to include in the URI
        :type query_params: dict or None
        :param payload_dict: Request body (JSON encodé en chaîne)
        :type payload: dict or None
        :param http_method: HTTP Method to use (warning GET doesn't support a payload)
        :type http_method: HTTPMethod
        :return: Réponse de l’API enrichie d’un champ "status"
        :rtype: dict
        """
        payload = self.create_payload(payload_dict) if payload_dict else None
        return self.__make_request(path, query_params, payload, http_method)
