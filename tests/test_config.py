import os.path
import unittest

from quads.config import _ConfigBase  # noqa


def get_mock_config():
    class Config(_ConfigBase):
        KEY = "value"

    return Config()


# noinspection PyUnresolvedReferences
class TestConfig(unittest.TestCase):
    def test_getattr(self):
        conf = get_mock_config()
        self.assertEqual(conf.KEY, "value")

        with self.assertRaises(AttributeError):
            _ = conf.NOT_EXISTS

    def test_getitem(self):
        conf = get_mock_config()
        self.assertEqual(conf["KEY"], "value")

        with self.assertRaises(KeyError):
            _ = conf["not_exists"]

    def test_load_yaml(self):
        test_yaml_path = os.path.join(os.path.dirname(__file__), "fixtures/test_conf.yaml")
        assert os.path.exists(test_yaml_path), f"Missing test fixture: {test_yaml_path}"

        conf = get_mock_config()
        conf.load_from_yaml(test_yaml_path)

        # Both in yaml and on class, class attr should not be overridden
        self.assertEqual(conf.KEY, "value")

        self.assertEqual(conf.other_key, "other_value")

        self.assertListEqual(conf.array, [1, "s", False])

        self.assertDictEqual(conf.dict, {"key1": "val1", "key2": "val2", "key3": "val3"})


if __name__ == "__main__":
    unittest.main()
