from datetime import datetime
import requests
import time
from abc import ABC, abstractmethod
from src.RequestFactory import RequestFactory


class GenericPipeline(ABC):
    """Abstract Pipeline class

    All Pipeline class must inherit from this class
    methods read, process and write needs to be override in the subclass

    """
    _data = None


    def load_data(self, data):
        """Check if data is an iterable and load data in self._data attribute

        if data argument hasn't __iter__ method implemented,
        ValueError is raised
        """
        if hasattr(data, '__iter__'):
            self._data = data
        else:
            raise ValueError("PyPipeline data must be a Generator or a Sequence(implement __iter__ method)")



    @abstractmethod
    def read(self, entry):
        """called in first for each element of the 'data' loaded (to parse)

        Arguments:

            entry:

                a data element that is passed through this function in run_pipe method
        """
        pass


    @abstractmethod
    def process(self, entry):
        """called in second for each element of the 'data' loaded (to process transformations)

            Arguments:

                entry:

                    a data element that is passed through this function in run_pipe method
        """
        pass


    @abstractmethod
    def write(self, entry_pack):
        """called in third for groups of elements of the 'data' loaded (to write it in base for example)

            Arguments:

                entry_pack:

                    a group of data element that is passed through this function in run_pipe method

        """
        pass


    def run_pipe(self, transaction_rate=None):
        """method to call to execute the pipe

        Arguments:

            transaction_rate(Optional):

                Integer.
                Provides the number of data elements that need to be write together
                with the write method
                Put it to 1(one) to write after each element process
                if transaction_rate number is higher than data length, write method
                is executed once for all data elements at the end
                if transaction_rate number is None(Not specified) write method is called
                once a the end of the pipe

        """
        # vide le cache d'erreur
        if hasattr(self, '_err_log'):
            self._err_log = []


        if transaction_rate is not None:
            count = 0
            data_storage = []
            for entry in self._data:
                data_fragment = self.read(entry)
                data_fragment = self.process(data_fragment)
                if data_fragment is not None:
                    data_storage.append(data_fragment)
                    count += 1

                if count == transaction_rate:
                    self.write(data_storage)
                    count = 0
                    data_storage = []

            if data_storage:
                self.write(data_storage)
        else:
            data_storage = []
            for entry in self._data:
                data_fragment = self.read(entry)
                data_fragment = self.process(data_fragment)
                if data_fragment is not None:
                    data_storage.append(data_fragment)
            if data_storage:
                self.write(data_storage)





class ApiPipeline(GenericPipeline, ABC):
    """ Abstract ApiPipeline

    All ApiPipeline class must inherit from this class
    methods read, process and write needs to be override in the subclass

    Arguments:

        request_factory(Required):

            RequestFactory instance (see the doc).
            A RequestFactory instance that will create all requests of the pipe


        sleeping_time(Optional):

            Float.
            If api calls need to be delayed, add the time in seconds you
            want that pipe sleep after each request to 'sleeping_time' argument
    """

    request_factory = None
    _err_log = []


    @property
    def err_log(self):
        """ List of errors occured during Pipe

            Log objects are 4-tuple like
                ("entry", "status_code_if_there_is", "datetime", "typeError")
            Errors catched are requests.exceptions.ConnectionError, Timeout, and HttpError
        """
        return [(str(err[0]), err[1], err[2], err[3]) for err in self._err_log]


    def err_params_log(self):
        """return error logs parameters to rerun the pipe with failed requests"""
        return [err[0].get_request_params() for err in self._err_log]


    def __init__(self, request_factory: RequestFactory, sleeping_time: float = None):
        if not isinstance(request_factory, RequestFactory):
            raise ValueError("request_factory argument needs to be an instance of RequestFactory")
        self.request_factory = request_factory
        self._sleeping_time = sleeping_time


    def read(self, entry):
        """wrap request parameters in the requestFactory

        create a request with a data element passed in argument
        and the requestFactory
        Data elements are not validated!
        data element need to be a 2-tuple (end_url:string, params:dict)

        Arguments:

            entry:

                a data element that is passed through this function in run_pipe method
                a correct data element for api call is

                    ("the end of the url", {"param_name":"param_val"})
                    or
                    ("the end of the url", None) if there is no params
                    or
                    (None, None) if there is no params and no end_url


        """
        read = self.request_factory(*entry)
        return read


    def process(self, entry):
        """execute the requests created by read() method and sleep if needed

        if an error Occurs during request execution an log object is added to
        err_log argument
        Log objects are 4-tuple like

                ("entry", "status_code_if_there_is", "datetime", "typeError")
        Errors catched are requests.exceptions.ConnectionError, Timeout, and HttpError

        Arguments:

            entry:

                a request element that is passed through this function in run_pipe method
                check read() method documentation
        """
        start_time = time.time()
        try:
            result = entry.get_response()
        except requests.exceptions.ConnectionError as e:
            self._err_log.append((entry, None, datetime.now(), "ConnectionError"), )
            result = None
        except requests.exceptions.Timeout as e:
            self._err_log.append((entry, None, datetime.now(), "TimeOut"), )
            result = None
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self._err_log.append((entry, result.status_code, datetime.now(), "HttpError"),)
            result = None

        if self._sleeping_time is not None and result is not None:
            run_time = time.time() - start_time
            if run_time < self._sleeping_time:
                time.sleep(self._sleeping_time - run_time)


        return result



    def __eq__(self, other):
        """Pipe with same request factorys are equals"""
        return self.request_factory == other.request_factory


    def __hash__(self):
        """Pipe with same request fatorys have same hash"""
        return hash(self.request_factory)


    def __repr__(self):
        return f"{self.__class__.__name__}(%r, %r)" % (self.request_factory, self._sleeping_time)



    @abstractmethod
    def write(self, entry_pack):
        """called in third for groups of elements of the 'data' loaded (to write it in base for example)

        You need to override this method. Provide the behavior you want for this data after the processing


        Arguments:

            entry_pack:

                a group of requests_results that is passed through this function in run_pipe method

        """
        pass









