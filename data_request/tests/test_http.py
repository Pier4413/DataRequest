import unittest
from unittest.mock import patch, Mock
from ..http import HTTP, HTTPMethod


class TestHTTP(unittest.TestCase):

    def setUp(self):
        self.client = HTTP(api_key="fake-key", host="example.com", port="80", is_ssl=False)

    @patch("requests.get")
    def test_get_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "ok"}
        mock_get.return_value = mock_response

        result = self.client.make_request(path="/test", http_method=HTTPMethod.GET)

        self.assertEqual(result["message"], "ok")
        self.assertEqual(result["status"], 200)
        mock_get.assert_called_once()

    @patch("requests.post")
    def test_post_success_with_payload(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"message": "created"}
        mock_post.return_value = mock_response

        payload = {"data": "test"}

        result = self.client.make_request(
            path="/create",
            http_method=HTTPMethod.POST,
            payload_dict=payload
        )

        self.assertEqual(result["message"], "created")
        self.assertEqual(result["status"], 201)
        mock_post.assert_called_once()

    def test_create_payload(self):
        data = {"hello": "world"}
        payload = self.client.create_payload(data)
        self.assertEqual(payload, '{"hello": "world"}')

    @patch("requests.get")
    def test_http_error_raises_exception(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("Erreur HTTP")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.client.make_request(path="/error", http_method=HTTPMethod.GET)

        self.assertIn("Échec de la requête", str(context.exception))

    @patch("requests.get")
    def test_connection_error(self, mock_get):
        mock_get.side_effect = Exception("Connexion impossible")

        with self.assertRaises(Exception) as context:
            self.client.make_request(path="/unreachable", http_method=HTTPMethod.GET)

        self.assertIn("Échec de la requête", str(context.exception))
