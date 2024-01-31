from tools.standard.communications.http import GET, POST


class HTTPMethods(GET, POST):
    @staticmethod
    def build_headers(access_token):
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        }
        if access_token:
            headers.update({'Authorization': f'Bearer {access_token}'})
        return headers
