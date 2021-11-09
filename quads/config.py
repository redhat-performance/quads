#!/usr/bin/env python3
import logging
import os

import yaml

logger = logging.getLogger(__name__)

DEFAULT_CONF_PATH = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")


class _ConfigBase:
    def load_from_yaml(self, filepath: str = DEFAULT_CONF_PATH):
        """
        Load values from yaml file as attributes of this class.
        Will never override existing attributes.
        """
        with open(filepath, "r") as config_file:
            conf = yaml.safe_load(config_file)
            assert type(conf) is dict

            for key, value in conf.items():
                if hasattr(self, key):
                    logger.warning(f"Key '{key}' is already defined on config class, not overriding")
                    continue
                setattr(self, key, value)

            logger.debug(f"Loaded yaml config from '{filepath}'")


class _Config(_ConfigBase):
    """
    Configuration "singleton"

    Class defined values should be considered globals (capitalized)
    and they always override values set in yaml.

    Examples:
        Config.QUADS_VERSION
        Config.email_host
    """

    LOGFMT = "%(asctime)-12s : %(levelname)-8s - %(message)s"
    STDFMT = "- %(levelname)-8s - %(message)s"

    API = "v2"

    @property
    def API_URL(self):
        return os.path.join(self.quads_base_url, "api", self.API)

    FPING_TIMEOUT = 10000

    QUADS_VERSION = "1.1.5"
    QUADS_CODENAME = "gaúcho"

    SUPPORTED = [
        "fc640",
        "r620",
        "r630",
        "r640",
        "640",
        "r650",
        "650",
        "r720",
        "r730xd",
        "r930",
        "r730",
        "r740xd",
        "740xd",
        "r720xd",
        "7425",
        "7525",
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


# Making sure there is exactly one instance of config used elsewhere
Config = _Config()

if __name__ == "__main__":
    # quick debug
    logging.basicConfig(level=logging.DEBUG)

    logger.info("Loading config file")
    Config.load_from_yaml(Config.DEFAULT_CONF_PATH)
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
