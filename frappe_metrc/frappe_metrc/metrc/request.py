import requests


DEFAULT_API_URL = "https://api-ca.metrc.com/"
SANDBOX_API_URL = "https://sandbox-api-ca.metrc.com/"
API_VERSION = "v1"

class METRC():
    def __init__(self, vendor_key, user_key, license, url):
        self.BASE_URL = url
        self.AUTH = (vendor_key, user_key)
        self.PARAMS = {"licenseNumber" : license}

    def post(self, endpoint, data=None):
        response = self._request(requests.post, endpoint, {"json": data})
        return response

    def get(self, endpoint, params=None):
        response = self._request(requests.get, endpoint, {"params" : params})
        if not response.status_code == 200:
            response.raise_for_status()
        else:
            return response.json()

    def delete(self, endpoint):
        response = self._request(requests.delete, endpoint)
        if response.status_code == 200:
            return response.json()

    def _request(self, method, endpoint, args=None):
        if args.get("params"):
            args.get("params").update(self.PARAMS)
        else:
            args["params"] = self.PARAMS

        return method(self._uri(endpoint), auth=self.AUTH, **args)

    def _uri(self, endpoint):
        return self.BASE_URL + endpoint
    
