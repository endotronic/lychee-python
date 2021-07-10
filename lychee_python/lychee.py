import requests
from requests.structures import CaseInsensitiveDict


class Lychee:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

        self.jar = requests.cookies.RequestsCookieJar()

    def request(self, function, data=None, files=None):
        url = "{0}/api/{1}".format(self.api_url, function)
        data = dict({"function": function}, **(data or {}))

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = self.api_key

        request = requests.post(
            url, headers=headers, cookies=self.jar, data=data, files=files
        )
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

    def get_album(self, album_id):
        return self.request(function="Album::get", data={"albumID": album_id})

    def add_album(self, title, parent_id=0):
        data = dict(title=title, parent_id=parent_id)
        return self.request(function="Album::add", data=data)

    def set_album_description(self, album_id, description):
        assert (
            self.request(
                function="Album::setDescription",
                data={"albumID": album_id, "description": description[:1000]},
            )
            == True
        )

    def add_photo(self, album_id, photo_data):
        data = {"albumID": album_id}
        files = {"0": photo_data}
        return self.request(function="Photo::add", data=data, files=files)

    def get_photo(self, photo_id):
        return self.request(function="Photo::get", data={"photoID": photo_id})

    def set_photo_tags(self, photo_id, tags):
        assert (
            self.request(
                function="Photo::setTags", data={"photoIDs": photo_id, "tags": tags}
            )
            == True
        )

    def set_photo_title(self, photo_id, title):
        assert (
            self.request(
                function="Photo::setTitle",
                data={"photoIDs": photo_id, "title": title[:100]},
            )
            == True
        )

    def set_photo_description(self, photo_id, description):
        assert (
            self.request(
                function="Photo::setDescription",
                data={"photoID": photo_id, "description": description},
            )
            == True
        )
