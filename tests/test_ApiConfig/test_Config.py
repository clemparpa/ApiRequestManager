from src.Config import Config


class TestConfig:

    objectEqual1 = Config(name="equal", base_url="test1", auth={"field": "token"})
    objectEqual2 = Config(name="equal", base_url="test2", headers={"header": "val"})

    objectAttr = Config(name="attr", base_url="test_attr", auth={"field": "attr"}, headers={"head": "atr"})



    def test_equality(self):

        assert self.objectEqual1 == self.objectEqual2


    def test_inequality(self):

        assert self.objectEqual1 != self.objectAttr


    def test_eq_hash(self):

        assert self.objectEqual1.__hash__() == self.objectEqual2.__hash__()


    def test_in_eq_hash(self):

        assert self.objectEqual2.__hash__() != self.objectAttr.__hash__()


    def test_attr(self):

        assert self.objectAttr.name == "attr"
        assert self.objectAttr.base_url == "test_attr"
        assert self.objectAttr.auth == {"field": "attr"}
        assert self.objectAttr.headers == {"head": "atr"}


    def test_repr(self):

        assert self.objectAttr.__repr__() == "Config(name='attr', base_url='test_attr', auth={'field': 'attr'}, headers={'head': 'atr'})"