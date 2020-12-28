from src.ApiRequest.ApiRequest import ApiRequest
from src.Config import Config



class TestApiRequest:

    Config_obj = Config(name="test_name",
                        base_url="https://jsonplaceholder.typicode.com",
                        auth={"auth_field": "auth_token"},
                        headers={"header1": "val1", "header2": "val2"})

    request_obj = ApiRequest()


    def test_set_config(self):

        self.request_obj.set_config(config=self.Config_obj)
        assert self.request_obj._headers == {"header1": "val1", "header2": "val2"}
        assert self.request_obj._auth == {"auth_field": "auth_token"}
        assert self.request_obj._base_url == "https://jsonplaceholder.typicode.com"



    def test_set_request(self):

        self.request_obj.set_request(end_url="todos/1")
        assert self.request_obj._end_url == "todos/1"



    def test_get_response(self):

        assert self.request_obj.get_response().json() == {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}

