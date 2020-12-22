
class ApiConfig:
    """class that store Api configuration added in ApiConfig instance

    Store Configs passed to ApiConfig and provide a search class
    method to retrieve configs by 'name'

    Exception:

        NotImplementedError:

            Call the '__init__' special method is not allowed
            it raises an Exception

    """

    configs: None


    def __init__(self):
        raise NotImplementedError(f" ApiConfigs class doesn't implement constructor. Don't try to call it")


    @classmethod
    def search(cls, api_name):
        """Classmethod to find Config object from 'name' attribute"""
        if cls.configs is None:
            raise ValueError("No Config provided in ApiConfig instance for search")
        for config in cls.configs:
            if config.name == api_name:
                return config
        raise ValueError("Api name not found in ApiConfig")











