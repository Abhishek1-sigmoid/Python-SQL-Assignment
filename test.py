import pytest
from connection import Connection

class TestEmployee:
    @classmethod
    def setup_class(cls):
        print("\nSetting Up Class")

    @classmethod
    def teardown_class(cls):
        print("\nTearing Down Class")

    @pytest.fixture
    def setup(self):
        obj = Connection()
        return obj

    def test_db_connection(self, setup):
        with pytest.raises(Exception):
            setup.get_connection("other", "pass")

    def test_engine(self, setup):
        with pytest.raises(Exception):
            setup.get_engine("other", "pass")



