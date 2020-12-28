from typing import List
from src.Pipelines import ApiPipeline
from src.RequestFactory import RequestFactory
from collections.abc import Callable
from functools import wraps


def instance_method_wrapper(func):
    """Decorator which return the same func with a 'self' argument in declaration"""
    @wraps(func)
    def decorated_(self, *args, **kwargs):
        return func(*args, **kwargs)
    return decorated_


def make_api_pipe(api_name: str, writer: Callable, sleeping_time: float = None):
    """ pipe maker for Api requests

    Arguments:

        api_name(Required):

            String.
            Api identifier bound to a Config name in ConfigPath (check Pipeline doc)

            ConfigPath(
                Config(name="random_name".......)
            )

            "random_name"  <-- api_name


        writer(Required):

            Callable which take an List(request.requests)  in argument.
            Function which override the ApiPipeline.write method (check ApiPipeline doc)


        sleeping_time(Optional):

            Float.
            The time in second to sleep between 2 requests (check Pipeline doc)


    Return:

        pipe_instance:

            An Instance of pipe (an ApiPipeline subclass with 'writer' arg that override ApiPipeline.write method)

    """
    pipe_cls = type("pipe_cls", (ApiPipeline, ), {"write": instance_method_wrapper(writer)})
    pipe_instance = pipe_cls(request_factory=RequestFactory(api_name), sleeping_time=sleeping_time)
    del pipe_cls
    return pipe_instance




def run_api_pipe(pipe_instance, request_arguments: List[tuple], retry_fails: bool = False, transaction_rate: int = None):
    """ pip runner to execute a pipe instance

    Arguments:

        pipe_instance(Required):

            An Instance of pipe (an ApiPipeline subclass with 'writer' arg that override ApiPipeline.write method)
            call make_api_pipe function to get a pipe_instance (see the doc above)


        request_arguments(Required):

            a list of 2-tuple elements like ("end_url", {"param_name": "param_val"})
            to provide request configurations check the RequestFactory doc


        retry_fails(Optional):

            Boolean.
            if put to 'True', request which failed will be executed a second time


        transaction_rate(Optional):

            Int.
            The number of request results to be passed to the pipe.write method each time
            if not configured, write method is executed once after all pipe requests processed
            check Pipeline Documentation



    Return:

        err_log:

            a log where are stored all requests informations which failed
            (2 times if 'retry_fails' argument is set to True)

    """
    retry = retry_fails
    pipe_instance.load_data(request_arguments)
    pipe_instance.run_pipe(transaction_rate=transaction_rate)
    log = pipe_instance.err_params_log()
    if retry:
        retry = False
        pipe_instance.load_data(log)
        pipe_instance.run_pipe(transaction_rate=transaction_rate)
    return pipe_instance.err_log



