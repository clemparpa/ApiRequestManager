from PyApiManager.ConfigPath import ConfigPath
from PyApiManager.Config import Config
from PyApiManager_src.ApiConfig.ApiConfig import ApiConfig
from PyApiManager.RequestFactory import RequestFactory
import pytest




@pytest.fixture(scope="session", autouse=True)
def create_path():
    config_path = ConfigPath(
            3,
            Config(name="config1", base_url="test1"),
            Config(name="config1", base_url="test1", auth={"field": "token"}),
            Config(name="test_factory", base_url="https://jsonplaceholder.typicode.com"),
            Config(name="config2", base_url="test2"),
            "foo"
        )



class TestRequestFactory:


    def test_request_creation(self):
        FactoryA = RequestFactory(api_name="test_factory")
        request_a = FactoryA(end_url="todos/1")
        assert request_a.json() == {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}




class TestConfigPath:


    def test_duplicates_config_type(self):

        assert ApiConfig.configs.sort(key=lambda x: x.name) == [
            Config(name="config1", base_url="test1"),
            Config(name="config2", base_url="test2"),
            Config(name="test_factory", base_url="https://jsonplaceholder.typicode.com"),
        ].sort(key=lambda x: x.name)



class TestApiConfig:


    def test_raise_init_error(self):

        with pytest.raises(NotImplementedError):
            ApiConfig()



    def test_raise_search_with_none_config(self):

        memo = ApiConfig.configs
        ApiConfig.configs = None
        with pytest.raises(ValueError):
            ApiConfig.search("foo")

        ApiConfig.configs = memo



    def test_raise_search_wrong_name(self):

        with pytest.raises(ValueError):
            ApiConfig.search("config3")



    def test_search(self):

        assert ApiConfig.search("config1") == Config(name="config1", base_url="test1")




