import requests


class GET:
    def get(self, uri, headers, query_params=None, auth=None):
        response = requests.get(uri, headers=headers, params=query_params, auth=auth)
        response.raise_for_status()
        return response.json()


class POST:
    def post(self, uri, headers, body):
        response = requests.post(uri, headers=headers, json=body)
        response.raise_for_status()
        return response.json()


class DELETE:
    def delete(self, uri, headers):
        response = requests.delete(uri, headers=headers)
        response.raise_for_status()
        return True


class HEAD:
    def head(self, uri, headers):
        response = requests.head(uri, headers=headers)
        response.raise_for_status()
        return True
