"""
Provide functions for reading and parsing configuration files.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

import json
import os

from pycbc.workflow import WorkflowConfigParser
from pycbc.distributions import read_params_from_config

from .staticargs import amend_static_args, typecast_static_args


# -----------------------------------------------------------------------------
# FUNCTION DEFINITIONS
# -----------------------------------------------------------------------------

def read_ini_config(file_path):
    """
    Read in a *.ini config file, which is used to specify the physical
    aspects of the waveform simulation.
    
    Args:
        file_path (str): Path to the *.ini config file to be read in.

    Returns:
        A tuple `(variable_arguments, static_arguments)` containing
        the variable and static arguments (names; and in the latter
        case also the values) defined in the specified config file.
    """
    
    # Make sure the config file actually exists
    if not os.path.exists(file_path):
        raise IOError('Specified configuration file does not exist: '
                      '{}'.format(file_path))
    
    # Set up a parser for the PyCBC config file
    workflow_config_parser = WorkflowConfigParser(configFiles=[file_path])
    
    # Read the variable_arguments and static_arguments using the parser
    variable_arguments, static_arguments = \
        read_params_from_config(workflow_config_parser)
    
    # Typecast and amend the static arguments
    static_arguments = typecast_static_args(static_arguments)
    static_arguments = amend_static_args(static_arguments)
    
    return variable_arguments, static_arguments


def read_json_config(file_path):
    """
    Read in a *.json config file, which is used to specify the
    "technical" aspects of the sample generation process.
    
    Args:
        file_path (str): Path to the *.json config file to be read in.

    Returns:
        A dictionary containing the contents of the given JSON file.
    """
    
    # Make sure the config file actually exists
    if not os.path.exists(file_path):
        raise IOError('Specified configuration file does not exist: '
                      '{}'.format(file_path))
    
    # Open the config while and load the JSON contents as a dict
    with open(file_path, 'r') as json_file:
        config = json.load(json_file)

    # Define the required keys for the config file in a set
    required_keys = {'background_data_directory', 'dq_bits', 'inj_bits',
                     'waveform_params_file_name', 'max_runtime',
                     'n_injection_samples', 'n_noise_samples', 'n_processes',
                     'random_seed', 'output_file_name'}
    
    # Make sure no required keys are missing
    missing_keys = required_keys.difference(set(config.keys()))
    if len(missing_keys) != 0:
        raise KeyError('Missing required key(s) in JSON configuration file: '
                       '\n{}'.format(', '.join(list(missing_keys))))

    return config