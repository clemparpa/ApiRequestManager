from PyApiManager_src.ApiRequest.ApiRequest import ApiRequest
from PyApiManager_src.ApiConfig.ApiConfig import ApiConfig
from PyApiManager.Config import Config


class RequestFactory:
    """RequestFactory creates generators of ApiRequest Instances



    Call a RequestFactory to create a request class for a particular
    api in referenced in the 'ConfigPath'



    __init__():


        api_name(Required):

            String.
            'name' argument of a Config instance stored
            in the ApiConfig
            --> see ApiConfig documentation
            --> see Config documentation

        creates a Factory

        ex

            FactoryA = RequestFactory(api_name="Api_A")



    __call__():


        end_url(Optional):

            String.
            Complete base_url request argument (from set_config)

            ex

                base_url = "https://api/"
                end_url = "end_of_url"

                --> url = "https://api/end_of_url"


        params(Optional):

            Dict.
            Parameters of the request url

            ex:
                params = {"plan":"Tier_one"}

                --> url = "https://api/end_of_url?plan=Tier_one"

            Multiple parameters can be provided by key/value pairs in this dict

        ex

            request1 = FactoryA(end_url=end_of_url, params={"plan":"Tier_one"})
            response = request1.json() <-- check 'requests' librairy  documentation
    """


    _config: Config
    _api_request: ApiRequest = ApiRequest()


    def __init__(self, api_name):
        self._api_name = api_name
        self._config = ApiConfig.search(api_name=self._api_name)
        self._api_request.set_config(self._config)


    def __call__(self, end_url=None, params=None):
        response = self._api_request.copy()
        response.set_request(end_url=end_url, params=params)
        return response.get_response()


    def __repr__(self):
        return "RequestFactory(%r)" % self._api_name





