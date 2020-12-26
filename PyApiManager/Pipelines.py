import time
from abc import ABC, abstractmethod
from PyApiManager.RequestFactory import RequestFactory


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
                if transaction_rate number is higher than data length, write method
                is executed once for all data elements at the end
                if transaction_rate number is None(Not specified) write method is called
                for each data element

        """
        if transaction_rate is not None:
            count = 0
            data_storage = []
            for entry in self._data:
                data_fragment = self.read(entry)
                data_fragment = self.process(data_fragment)
                data_storage.append(data_fragment)
                count += 1

                if count == transaction_rate:
                    self.write(data_storage)
                    count = 0
                    data_storage = []

            if data_storage:
                self.write(data_storage)
        else:
            for entry in self._data:
                data_fragment = self.read(entry)
                data_fragment = self.process(data_fragment)
                self.write([data_fragment])




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

    _RequestFactory = None


    def __init__(self, request_factory: RequestFactory, sleeping_time: float = None):
        if not isinstance(request_factory, RequestFactory):
            raise ValueError("request_factory argument needs to be an instance of RequestFactory")
        self._RequestFactory = request_factory
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
        read = self._RequestFactory(*entry)
        return read


    def process(self, entry):
        """execute the requests created by read() method and sleep if needed

        Arguments:

            entry:

                a request element that is passed through this function in run_pipe method
                check read() method documentation

        """
        result = entry.get_response()
        if self._sleeping_time is not None:
            time.sleep(self._sleeping_time)
        return result


    @abstractmethod
    def write(self, entry_pack):
        """called in third for groups of elements of the 'data' loaded (to write it in base for example)

        You need to override this method. Provide the behavior you want for this data after the processing


        Arguments:

            entry_pack:

                a group of requests_results that is passed through this function in run_pipe method

        """
        pass






