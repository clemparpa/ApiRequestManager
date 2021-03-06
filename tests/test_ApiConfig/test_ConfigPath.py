from src.ConfigPath import ConfigPath
from src.Config import Config
from src.ApiConfig.ApiConfig import ApiConfig
from src.RequestFactory import RequestFactory
from src.Pipelines import ApiPipeline
from src.make_pipe import make_api_pipe, run_api_pipe
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



class TestApiPipeImperativFunctions:

    data_store = []


    class PipeCls(ApiPipeline):
        data_store = []

        def write(self, entry_pack):
            self.data_store.append([item.json() for item in entry_pack])


    def write(self, entry_pack):
        self.data_store.append([item.json() for item in entry_pack])

    real_entry_list = [
        ("todos/1", None),
        ("todos/1", None),
        ("todos/1", None),
        ("todos/1", None),
        ("fake_url_for_test", None)
    ]

    def test_make_api_pipe_equals_results(self):

        real_factory = RequestFactory("test_factory")
        imperativ_pipe = make_api_pipe("test_factory", writer=self.write, sleeping_time=0.1)
        class_pipe = self.PipeCls(real_factory, 0.1)
        assert imperativ_pipe.err_params_log() == class_pipe.err_params_log()



    def test_run_api_pipe(self):
        pipe = make_api_pipe("test_factory", writer=self.write, sleeping_time=0.1)
        run_api_pipe(pipe, self.real_entry_list, retry_fails=True)
        assert self.data_store == [
            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],
        ]

    def test_retries_api_pipe(self):
        pipe = make_api_pipe("test_factory", writer=self.write, sleeping_time=0.1)
        run_api_pipe(pipe, self.real_entry_list, retry_fails=True)

        assert pipe.err_params_log() == [("fake_url_for_test", None),]



class TestApiPipeline:


    class PipeCls(ApiPipeline):
        data_store = []

        def write(self, entry_pack):
            self.data_store.append([item.json() for item in entry_pack])


    fake_factory = "fake_factory"

    real_entry_list = [
        ("todos/1", None),
        ("todos/1", None),
        ("todos/1", None),
        ("todos/1", None),
        ("fake_url_for_test", None)
    ]

    real_entry_gen = (item for item in real_entry_list)
    fake_entry = 667



    def test_fake_factory_pipe_init(self):

        with pytest.raises(ValueError):
            self.PipeCls(self.fake_factory)


    def test_true_factory_pipe_init(self):
        real_factory = RequestFactory("test_factory")
        assert self.PipeCls(real_factory).request_factory == real_factory


    def test_fake_load_data(self):
        real_factory = RequestFactory("test_factory")
        with pytest.raises(ValueError):
            self.PipeCls(real_factory).load_data(self.fake_entry)


    def test_real_load_data_list(self):
        real_factory = RequestFactory("test_factory")
        pipe = self.PipeCls(real_factory)
        pipe.load_data(self.real_entry_list)
        assert pipe._data == self.real_entry_list


    def test_real_load_data_gen(self):
        real_factory = RequestFactory("test_factory")
        pipe = self.PipeCls(real_factory)
        pipe.load_data(self.real_entry_gen)
        assert pipe._data == self.real_entry_gen



    def test_no_transaction_rate(self):
        real_factory = RequestFactory("test_factory")
        pipe = self.PipeCls(real_factory)
        pipe.load_data(self.real_entry_list)
        pipe.run_pipe()
        assert pipe.data_store == [
            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],
        ]


    def test_transaction_rate(self):
        real_factory = RequestFactory("test_factory")
        pipe = self.PipeCls(real_factory)
        pipe.load_data(self.real_entry_list)
        pipe.run_pipe(transaction_rate=2)
        assert pipe.data_store == [
            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],

            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],
            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],
        ]


    def test_higher_transaction_rate(self):
        real_factory = RequestFactory("test_factory")
        pipe = self.PipeCls(real_factory, 0.3)
        pipe.load_data(self.real_entry_list)
        pipe.run_pipe(10)
        assert pipe.data_store == [
            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],

            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],
            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],

            [{'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1},
             {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}],
        ]

    def test_err_log(self):
        real_factory = RequestFactory("test_factory")
        pipe = self.PipeCls(real_factory, 0.3)
        pipe.load_data(self.real_entry_list)
        pipe.run_pipe()
        assert pipe.err_log != []


    def test_eq_pipes(self):
        real_factory = RequestFactory("test_factory")
        pipe1 = self.PipeCls(real_factory, 0.3)
        pipe2 = self.PipeCls(real_factory, 1)

        assert pipe1 == pipe2
        assert hash(pipe1) == hash(pipe2)

    def test_repr(self):
        real_factory = RequestFactory("test_factory")
        pipe = self.PipeCls(real_factory, 0.3)
        assert str(pipe) == "PipeCls(RequestFactory('test_factory'), 0.3)"





class TestRequestFactory:


    def test_request_creation(self):
        FactoryA = RequestFactory(api_name="test_factory")
        request_a = FactoryA(end_url="todos/1")
        assert request_a.get_response().json() == {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}




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




