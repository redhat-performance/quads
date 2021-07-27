#!/usr/bin/env python3
import logging
import os
import types
import warnings
from typing import Optional, Any

import yaml

logger = logging.getLogger(__name__)


class classproperty:
    """
    Class properties
    """

    def __init__(self, fget):
        self._fget = fget

    def __get__(self, _owner_self, owner_cls):
        return self._fget(owner_cls)


class SingletonIntegrityError(TypeError):
    pass


class YamlConfigSingleton(type):
    """
    Metaclass for configuration singleton with support
    for loading values from yaml files

    Values from the yaml file are populated as attributes
    of the final class. Class set values shadow values from yaml file.

    Supports both attribute and subscription/getitem access
    (though, generally there should be one and only one exact
    way to do this, but for now this is easier due to compatibility)

    There is a lot of defensive checks included to avoid
    accidentally shooting yourself in the leg later
    (read-only, internal value access thru subscription, ...)
    """

    _yaml_loaded: bool = False

    def load_yaml_file(self, path: str):
        """
        Populates attributes of the class with values from yaml file

        :param path: path to yaml file
        :raises FileNotFoundError:
        :raises yaml.YAMLError:
        """

        if self._yaml_loaded:
            logger.warning("Yaml file already loaded, multiple calls to load_yaml_file?")

        with open(path, "r") as config_file:
            conf = yaml.safe_load(config_file)
            assert type(conf) is dict

            for key, value in conf.items():
                if hasattr(self, key):
                    logger.warning(f"Duplicate key '{key}' loaded from yaml file, ignoring")
                    continue

                super(YamlConfigSingleton, self).__setattr__(key, value)

            logger.debug(f"Loaded yaml config '{path}'")

        super(YamlConfigSingleton, self).__setattr__("_yaml_loaded", True)

    @staticmethod
    def _validate_key(key):
        """
        Integrity checks for accessing keys
        :raises SingletonIntegrityError:
        :raises TypeError:
        """
        if not isinstance(key, str):
            raise TypeError(f"Invalid key type '{type(key)}', only string keys are supported")

        if key.startswith("_"):
            raise SingletonIntegrityError(f"Invalid key: '{key}', cannot access internal values ")

    @staticmethod
    def _validate_value(value):
        """
        Integrity checks for returned values
        :raises SingletonIntegrityError:
        """
        if type(value) in (types.MethodType, types.FunctionType):
            raise SingletonIntegrityError("Cannot access bound methods thru subscription")

    def get(self, key: str, *default) -> Optional[Any]:
        """
        Get value by key in config, with optional default

        :param key: string value
        :param default: Optional default value to return if key not found
        :raises KeyError: If key is not found and default is not supplied
        """

        # Implementing get(key, default) is harder then it seems
        # doing 'default=None' would make it impossible
        # to distinguish if that's the value to return as default
        # or that the argument was not passed at all and raise KeyError

        if default and len(default) != 1:
            raise TypeError("Too many arguments in get call, expected at maximum 2")

        self._validate_key(key)

        try:
            value = getattr(self, key)
        except AttributeError as exc:
            if not default:
                raise KeyError(exc)
            value = default[0]

        self._validate_value(value)

        return value

    def __getitem__(self, key: str):
        self._validate_key(key)

        try:
            value = getattr(self, key)
        except AttributeError as err:
            raise KeyError(key) from err

        self._validate_value(value)

        return value

    def __getattribute__(self, item):
        try:
            return super(YamlConfigSingleton, self).__getattribute__(item)
        except AttributeError as err:
            if not self._yaml_loaded:
                warnings.warn("Yaml file is not loaded yet")
            raise err

    def __contains__(self, item: str):
        return item in self.__dict__

    def __setattr__(self, key, value):
        """
        Making sure this object cannot be accidentally edited
        on runtime as it is shared thru out the code.
        """
        raise TypeError(f"{self.__class__.__name__} is read only")


# noinspection PyMethodParameters
class Config(metaclass=YamlConfigSingleton):
    """
    Configuration singleton, read-only
    Combines both yaml loaded values and values from class attributes

    Class defined values should be considered globals (capitalized)
    and they always override values set in yaml

    Examples:
        QConfig.QUADS_VERSION
        QConfig.email_host
        Qconfig["exclude_hosts"]
        QConfig.get("API", "v2")
        "key" in QConfig
    """

    DEFAULT_CONF_PATH = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")

    QUADS_VERSION = "1.1.5"
    QUADS_CODENAME = "gaúcho"

    SUPPORTED = [
        "fc640",
        "r620",
        "r630",
        "r640",
        "640",
        "r720",
        "r730xd",
        "r930",
        "r730",
        "r740xd",
        "740xd",
        "r720xd",
    ]
    OFFSETS = {"em1": 0, "em2": 1, "em3": 2, "em4": 3, "em5": 4}
    TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates")
    INTERFACES = {
        "em1": ["172.16", "172.21"],
        "em2": ["172.17", "172.22"],
        "em3": ["172.18", "172.23"],
        "em4": ["172.19", "172.24"],
        "em5": ["172.20", "172.25"],
    }

    LOGFMT = "%(asctime)-12s : %(levelname)-8s - %(message)s"
    STDFMT = "- %(levelname)-8s - %(message)s"

    API = "v2"

    @classproperty
    def API_URL(cls):
        return os.path.join(cls.quads_base_url, "api", cls.API)


if __name__ == "__main__":
    # quick debug
    logging.basicConfig(level=logging.DEBUG)

    logger.info("Loading config file")
    Config.load_yaml_file(Config.DEFAULT_CONF_PATH)
    logger.info("File loaded ok")

    logger.debug(Config.API_URL)
    logger.debug(Config.visual_colors)

    logger.debug(Config.get("API_URL", None))
    logger.debug(Config.get("NOPE_KEY", "YEP_VALUE"))

    logger.debug("NOPE_KEY" in Config)
    logger.debug("API_URL" in Config)
    logger.debug("email_notify" in Config)

    try:
        Config.test = 1
    except Exception as exc:
        logger.debug(exc, exc_info=exc)

    try:
        _ = Config.NOT_EXISTS
    except Exception as exc:
        logger.debug(exc, exc_info=exc)

    try:
        _ = Config["NOT_EXISTS_GETITEM"]
    except Exception as exc:
        logger.debug(exc, exc_info=exc)
