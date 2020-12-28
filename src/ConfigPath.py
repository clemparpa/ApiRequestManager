from src.ApiConfig.UniqueDecorator import Unique
from src.Config import Config
from src.ApiConfig.ApiConfig import ApiConfig


@Unique
class ConfigPath:
    """Path which accept Config objects

    Implement ApiConfigs class by '__init__' special method
    Only Config objects are allowed(others are deleted, No Exception raised)
    Config Objects with unique 'name' attributs(if duplicates, one is saved others deleted)



    Arguments:

        config:

            Config Object which provide api configuration
            ApiConfig accept multiple Config Objects, separated by comma
            ex

                ApiConfig(
                        Config(
                        name="Api1",
                        base_url="https://api/",
                        auth=None,
                        headers={'header_field':'header_value'}),

                        Config(
                        name="Api1",
                        base_url="https://api/",
                        auth={'auth_field':'auth_token'},
                        headers=None),
                    )

            Specify 'None' is not required when optional argument do not need a value


    Exception:

        UserWarning:

            Only One ApiConfig instanciation allowed
            If two 'ApiConfig()' declared in your code
            UserWarning Error is raised

    """


    def __init__(self, *configs):
        ApiConfig.configs = list(set([api for api in configs if isinstance(api, Config)]))


    def __repr__(self):
        return "ApiConfig( *%r)" % ApiConfig.configs



