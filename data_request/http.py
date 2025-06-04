import json
import requests
from enum import Enum
from typing import Optional
from urllib.parse import urljoin

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

    def __init__(self, api_key: str, host: str, port: str, is_ssl: bool = False) -> None:
        """
        Initialise le client HTTP.

        :param api_key: Clé API pour l'authentification
        :type api_key: str
        :param host: Nom d'hôte du serveur
        :type host: str
        :param port: Port de connexion de l'API
        :type port: str
        :param is_ssl: True pour utiliser HTTPS, False pour HTTP
        :type is_ssl: bool
        """
        protocol = "https" if is_ssl else "http"
        self.api_key = api_key
        self.base_url = f"{protocol}://{host}:{port}"

    def __make_request(
        self,
        path: str,
        query_params: Optional[dict] = None,
        payload: Optional[str] = None,
        http_method: HTTPMethod = HTTPMethod.GET
    ) -> dict:
        """
        Effectue la requête HTTP.

        :param path: Chemin de l'endpoint (ex : "/api/status")
        :type path: str
        :param query_params: Paramètres à inclure dans l'URL
        :type query_params: dict or None
        :param payload: Corps de la requête (JSON encodé en chaîne)
        :type payload: str or None
        :param http_method: Méthode HTTP à utiliser
        :type http_method: HTTPMethod
        :return: Réponse de l’API sous forme de dictionnaire avec un champ "status"
        :rtype: dict
        :raises Exception: En cas d’erreur réseau ou de réponse invalide
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
                    response = requests.get(url, headers=headers, params=query_params)
                case HTTPMethod.POST:
                    response = requests.post(url, headers=headers, params=query_params, data=payload)
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
        Sérialise un dictionnaire en chaîne JSON.

        :param payload_dict: Dictionnaire à convertir en JSON
        :type payload_dict: dict
        :return: Représentation JSON sous forme de chaîne
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
        Envoie une requête HTTP à l’API avec ou sans charge utile.

        :param path: Chemin de l’endpoint
        :type path: str
        :param query_params: Paramètres à inclure dans l’URL
        :type query_params: dict or None
        :param payload_dict: Dictionnaire à envoyer dans le corps de la requête
        :type payload_dict: dict or None
        :param http_method: Méthode HTTP à utiliser
        :type http_method: HTTPMethod
        :return: Réponse de l’API enrichie d’un champ "status"
        :rtype: dict
        """
        payload = self.create_payload(payload_dict) if payload_dict else None
        return self.__make_request(path, query_params, payload, http_method)
