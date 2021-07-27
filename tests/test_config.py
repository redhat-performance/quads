import os.path
import unittest

from quads.config import YamlConfigSingleton, classproperty, SingletonIntegrityError


def get_mock_conf():
    class MockConfig(metaclass=YamlConfigSingleton):
        KEY = "value"

        @classproperty
        def TEST_PROP(cls):
            return f"{cls.KEY}_prop"

    return MockConfig


# noinspection PyUnresolvedReferences
class TestConfig(unittest.TestCase):
    def test_getattr(self):
        conf = get_mock_conf()
        self.assertEqual(conf.KEY, "value")

        with self.assertRaises(AttributeError):
            _ = conf.NOT_EXISTS

    def test_getitem(self):
        conf = get_mock_conf()
        self.assertEqual(conf["KEY"], "value")

        with self.assertRaises(KeyError):
            _ = conf["NOT_EXISTS"]

        # Invalid access to internal values

        with self.assertRaises(SingletonIntegrityError):
            _ = conf["load_yaml_file"]

        with self.assertRaises(SingletonIntegrityError):
            _ = conf["_yaml_loaded"]

    def test_config_get(self):
        conf = get_mock_conf()

        # Valid
        self.assertEqual(conf.get("KEY"), conf.KEY)
        self.assertEqual(conf.get("KEY", None), conf.KEY)

        # Missing
        self.assertEqual(conf.get("not_exists", None), None)

        with self.assertRaises(KeyError):
            conf.get("not_exists")

        with self.assertRaises(SingletonIntegrityError):
            conf.get("load_yaml_file")

    def test_is_readonly(self):
        conf = get_mock_conf()

        with self.assertRaises(TypeError):
            # test attribute set value
            conf.KEY = False

        with self.assertRaises(TypeError):
            # test yaml loaded value
            conf.other = False

        with self.assertRaises(TypeError):
            conf["other"] = "value"

    def test_classproperty(self):
        conf = get_mock_conf()
        self.assertEqual(conf.TEST_PROP, "value_prop")

    def test_load_yaml(self):
        test_yaml_path = os.path.join(os.path.dirname(__file__), "fixtures/test_conf.yaml")
        assert os.path.exists(test_yaml_path), f"Missing test fixture: {test_yaml_path}"

        conf = get_mock_conf()
        conf.load_yaml_file(test_yaml_path)

        # Both in yaml and on class
        self.assertEqual(conf.KEY, "value")

        self.assertEqual(conf.other_key, "other_value")
        self.assertEqual(conf["other_key"], "other_value")

        self.assertListEqual(conf.array, [1, "s", False])
        self.assertListEqual(conf["array"], [1, "s", False])

        self.assertDictEqual(conf.dict, {"key1": "val1", "key2": "val2", "key3": "val3"})
        self.assertDictEqual(conf["dict"], {"key1": "val1", "key2": "val2", "key3": "val3"})

        with self.assertRaises(AttributeError):
            _ = conf.not_exists


if __name__ == "__main__":
    unittest.main()
