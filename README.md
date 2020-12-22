# PyApiManager
 Communicate with Apis with flow


PyApiManager module provides ConfigPath object and RequestFactory to be able
to call many apis easily


## documentation 
https://clemparpa.github.io

## PyPi project page
https://test.pypi.org/project/PyApiManager-clemparpa/0.5.1/


## Demo

Create a Config Path Instance which contains configurations for your apis: 

    ConfigPath(
        Config(name="api_demo", base_url="https://api_demo_url"),
        Config(name="api_2_demo", base_url="http://api_2_demo_base")
    )
    
Then Create Request Classes for your apis

    ApiDemo = RequestFactory(api_name="api_demo")
    Api2Demo = RequestFactory(api_name="api_2_demo")
    
Finally instanciate and execute requests

    response = ApiDemo(end_url="clemparpa")
    response2 = Api2Demo(end_url="Zlatan")
    response3 = ApiDemo(end_url="Neymar", params={"league":"2021392"})

It return requests.request objects for the following urls

    response ---> "GET" https://api_demo_url/clemparpa
    response2 ---> "GET" http://api_2_demo_base/Zlatan
    response3 ---> "GET" https://api_demo_url/Neimar?league=2021392

if it's JSON format data, response.json() returns a dict which contains data


