__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "arenas.guerrero.julian@outlook.com"


import argparse

from configparser import ExtendedInterpolation

from .utils import configure_logger
from .config import Config




def _parse_arguments():
    """
    Parses command line arguments.
    """

    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        prog='python3 -m rml_fnml_translator',
        argument_default=argparse.SUPPRESS
    )

    parser.add_argument('-i', '--input', help='path to the input [R2]RML+FnO mappings')
    parser.add_argument('-o', '--output', help='path to the output [R2]RML mappings')
    parser.add_argument('-m', '--mapping_language', help='whether to generate R2RML or RML (valid options: `R2RML` or `RML`)')
    parser.add_argument('-v', '--version', action='version',
                        version=f'rml-fnml-translator 0.1.0')

    return parser.parse_args()


def _parse_config(config):
    """
    Parses the config file. Logger is configured.
    """

    config.complete_configuration_with_defaults()
    config.validate_configuration_section()

    configure_logger(config.get_logging_level(), config.get_logging_file())
    config.log_config_info()

    return config


def load_config_from_command_line():
    """
    Parses command line arguments.
    """

    args = _parse_arguments()

    config = Config(interpolation=ExtendedInterpolation())

    config_entry = f'[CONFIGURATION]\nlogging_level=ERROR\n[data_source]\nmappings={args.input}\noutput={args.output}\nmapping_language={args.mapping_language}'
    config.read_string(config_entry)

    config = _parse_config(config)

    return config