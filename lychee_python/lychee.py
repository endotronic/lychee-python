import requests
from requests.structures import CaseInsensitiveDict


class Lychee:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

        self.jar = requests.cookies.RequestsCookieJar()

    def request(self, function, data=None):
        url = "{0}/api/{1}".format(self.api_url, function)
        data = dict({"function": function}, **(data or {}))

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = self.api_key

        request = requests.post(url, headers=headers, cookies=self.jar, data=data)
        if request.status_code != 200:
            raise Exception(
                "Got status {} for function {}".format(request.status_code, function)
            )
        self.jar = request.cookies
        return request.json()

    def login(self, username, password):
        assert (
            self.request(
                function="Session::login",
                data={
                    "username": username,
                    "password": password,
                },
            )
            == True
        ), "Incorrect credentials?"

    def get_albums(self):
        return self.request(function="Albums::get")

    def add_album(self, title, parent_id=0):
        data = dict(title=title, parent_id=parent_id)
        return self.request(function="Album::add", data=data)
