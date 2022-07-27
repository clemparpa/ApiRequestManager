# ApiRequestManager
 Communicate with Apis with easily

ApiRequestManager module provides ConfigPath object and RequestFactory to be able
to call many apis easily


## documentation 
https://clemparpa.github.io


## Github source page
https://github.com/clemparpa/ApiRequestManager


## PyPi project page
https://pypi.org/project/ApiRequestManager/1.0.4/


## Install
    
    pip install ApiRequestManager==1.0.4


## Usage

Create a Config Path Instance which contains configurations for your apis: 

 ```python
     from ApiRequestManager import Config, ConfigPath


     ConfigPath(
         Config(name="api_demo", base_url="https://api_demo_url"),
         Config(name="api_2_demo", base_url="http://api_2_demo_base")
     )
 ```
    
Then Create Request Classes for your apis

 ```python
    from ApiRequestManager import RequestFactory 

    ApiDemoFacotory = RequestFactory(api_name="api_demo")
    Api2DemoFacotory = RequestFactory(api_name="api_2_demo")
 ```
    
Finally instanciate and execute requests

 ```python
    response =  ApiDemoFacotory(end_url="clemparpa")
    response2 = Api2DemoFacotory(end_url="Zlatan")
    response3 = ApiDemoFacotory(end_url="Neymar", params={"league":"2021392"})
 ```

It return requests.request objects for the following urls

    response ---> "GET" https://api_demo_url/clemparpa
    response2 ---> "GET" http://api_2_demo_base/Zlatan
    response3 ---> "GET" https://api_demo_url/Neimar?league=2021392

if it's JSON format data, response.get_response().json() returns a dict which contains data

You can either use a Pipeline to execute many requests in a batch:

import the pipeline classes

 ```python
    from ApiRequestManager import ApiPipeline
 ```

then create your pipeline by inheriting ApiPipeline class (check documentation) 

you need to override write method.

here it just print the pipe results
    
 ```python
    class DemoPrintPipeline(ApiPipeline):
    
        def write(entry_pack):
            print(entry_pack)
 ```

create a instance of the class designed            

here a pipe with the ApiDemoFactory as RequestFactory and 1 second for sleeping time

(check pipelines documentation)

 ```python
    pipe = DemoPrintPipeline(ApiDemoFacotory, sleeping_time=1)
 ```
 
loading requests parameters:
 
 ```python
    parameters = [
            ("clemparpa", None),
            ("Neymar", {"league":"2021392"})
        ]

    pipe.load_data(parameters)
 ```
 
run the pipe:

 ```python
    pipe.run_pipe()
 ```
 
execute two requests with 1 second sleeping between:

    >>> "GET" https://api_demo_url/clemparpa
    >>> "GET" https://api_demo_url/Neimar?league=2021392


You can also use these 2 next functions for the same result
 
 ```python
    from ApiRequestManager import make_api_pipe, run_api_pipe
    
    demo_pipe = make_api_pipe(api_name="api_demo",
                              writer=lambda entry_pack: print(entry_pack),
                              sleeping_time=1)
    
    log = run_api_pipe(pipe_instance=demo_pipe,
                       request_arguments=parameters)
 ```                       

the log variable store a containing requests which failed
   


## Coverage

     -- coverage: platform win32, python 3.8.1-final-0 --
    Name                               Stmts   Miss  Cover
    ------------------------------------------------------
    ApiRequestManager\__init__.py               6      6     0%
    src\ApiConfig\ApiConfig.py            12      0   100%
    src\ApiConfig\UniqueDecorator.py      17      3    82%
    src\ApiConfig\__init__.py              0      0   100%
    src\ApiRequest\ApiRequest.py          51      4    92%
    src\ApiRequest\__init__.py             0      0   100%
    src\Config.py                         16      0   100%
    src\ConfigPath.py                      9      1    89%
    src\Pipelines.py                      88     10    89%
    src\RequestFactory.py                 16      0   100%
    src\__init__.py                        0      0   100%
    src\make_pipe.py                      25      0   100%
    ------------------------------------------------------
    TOTAL                                240     24    90%



coverage report with pytest-cov
