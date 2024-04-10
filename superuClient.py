import json
import httpx
from base64 import b64encode
from serializer import EventSerializer

class SuperUClient:
    _public_key: str
    _secret_key: str
    _base_url: str
    _version: str
    _timeout: int
    _session: httpx.Client

    def __init__(
        self,
        public_key: str,
        secret_key: str,
        base_url: str,
        version: str,
        timeout: int,
        session: httpx.Client,
    ):
        self._public_key = public_key
        self._secret_key = secret_key
        self._base_url = base_url
        self._version = version
        self._timeout = timeout
        self._session = session

    def generate_headers(self):
        return {
            "Authorization": "Basic "
            + b64encode(
                f"{self._public_key}:{self._secret_key}".encode("utf-8")
            ).decode("ascii"),
            "Content-Type": "application/json",
            "x_langfuse_sdk_name": "python",
            "x_langfuse_sdk_version": self._version,
            "x_langfuse_public_key": self._public_key,
        }

    def batch_post(self, **kwargs) -> httpx.Response:
        """Post the `kwargs` to the batch API endpoint for events"""

        # logging.debug("uploading data: %s", kwargs)
        res = self.post(**kwargs)
        return self._process_response(
            res, success_message="data uploaded successfully", return_json=False
        )

    def post(self, **kwargs) -> httpx.Response:
        """Post the `kwargs` to the API"""
        # log = logging.getLogger("langfuse")
        url = self._remove_trailing_slash(self._base_url) + "/api/public/ingestion"
        data = json.dumps(kwargs, cls=EventSerializer)
        # log.debug("making request: %s to %s", data, url)
        headers = self.generate_headers()
        res = self._session.post(
            url, content=data, headers=headers, timeout=self._timeout
        )

        if res.status_code == 200:
            print("data uploaded successfully")

        return res

    def _remove_trailing_slash(self, url: str) -> str:
        """Removes the trailing slash from a URL"""
        if url.endswith("/"):
            return url[:-1]
        return url