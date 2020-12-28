from src.ApiConfig.UniqueDecorator import Unique
from pytest import raises


@Unique
class Foo:

    def __init__(self):
        pass

    def __repr__(self):
        return "Foo repr"

    def __doc__(self):
        return "Foo doc"

    def __str__(self):
        return "Foo str"


@Unique
class Bar:

    def __init__(self):
        pass

    def __repr__(self):
        return "Bar repr"

    def __doc__(self):
        return "Bar doc"

    def __str__(self):
        return "Bar str"



class TestUnique:


    def test_duplicate_raise_user_warning(self):

        with raises(UserWarning):
            a = Foo()
            b = Foo()


    def test_repr_str_doc(self):

        c = Bar()

        assert c.__repr__() == "Bar repr"
        assert c.__doc__() == "Bar doc"
        assert c.__str__() == "Bar str"