# PyApiManager
 Communicate with Apis with flow


PyApiManager module provides ConfigPath object and RequestFactory to be able
to call many apis easily


## documentation 
https://clemparpa.github.io

## PyPi project page
https://test.pypi.org/project/PyApiManager-clemparpa/0.7.1/


## Install
    
    pip install -i https://test.pypi.org/simple/ PyApiManager-clemparpa==0.7.1


## Usage

Create a Config Path Instance which contains configurations for your apis: 

    from PyApiManager import Config, ConfigPath


    ConfigPath(
        Config(name="api_demo", base_url="https://api_demo_url"),
        Config(name="api_2_demo", base_url="http://api_2_demo_base")
    )
    
Then Create Request Classes for your apis

    from PyApiManager import RequestFactory 

    ApiDemoFacotory = RequestFactory(api_name="api_demo")
    Api2DemoFacotory = RequestFactory(api_name="api_2_demo")
    
Finally instanciate and execute requests

    response =  ApiDemoFacotory(end_url="clemparpa")
    response2 = Api2DemoFacotory(end_url="Zlatan")
    response3 = ApiDemoFacotory(end_url="Neymar", params={"league":"2021392"})

It return requests.request objects for the following urls

    response ---> "GET" https://api_demo_url/clemparpa
    response2 ---> "GET" http://api_2_demo_base/Zlatan
    response3 ---> "GET" https://api_demo_url/Neimar?league=2021392

if it's JSON format data, response.get_response().json() returns a dict which contains data

You can either use a Pipeline to execute many requests in a batch:

import the pipeline classes


    from PyApiManager import ApiPipeline


then create your pipeline by inheriting ApiPipeline class (check documentation) 

you need to override write method.

here it just print the pipe results
    

    class DemoPrintPipeline(ApiPipeline):
    
        def write(entry_pack):
            print(entry_pack)

create a instance of the class designed            

here a pipe with the ApiDemoFactory as RequestFactory and 1 second for sleeping time

(check pipelines documentation)
    
    pipe = DemoPrintPipeline(ApiDemoFacotory, sleeping_time=1)

loading requests parameters:

    parameters = [
            ("clemparpa", None),
            ("Neymar", {"league":"2021392"})
        ]

    pipe.load_data(parameters)
        
run the pipe:

    pipe.run_pipe()
    
execute two requests with 1 second sleeping between:

    >>> "GET" https://api_demo_url/clemparpa
    >>> "GET" https://api_demo_url/Neimar?league=2021392




## Coverage

    ----------- coverage: platform win32, python 3.8.1-final-0 -----------
    Name                                            Stmts   Miss  Cover
    -------------------------------------------------------------------
    PyApiManager\Config.py                             16      0   100%
    PyApiManager\ConfigPath.py                          9      1    89%
    PyApiManager\Pipelines.py                          84     10    88%
    PyApiManager\RequestFactory.py                     16      0   100%
    PyApiManager\__init__.py                            5      0   100%
    PyApiManager_src\ApiConfig\ApiConfig.py            12      0   100%
    PyApiManager_src\ApiConfig\UniqueDecorator.py      17      3    82%
    PyApiManager_src\ApiConfig\__init__.py              0      0   100%
    PyApiManager_src\ApiRequest\ApiRequest.py          49      4    92%
    PyApiManager_src\ApiRequest\__init__.py             0      0   100%
    PyApiManager_src\__init__.py                        0      0   100%
    -------------------------------------------------------------------
    TOTAL                                             208     18    91%



coverage report with pytest-cov
