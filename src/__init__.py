# src/__init__.py

# This file makes the src directory a Python package.

# You can include package-level imports here if needed.
# For example, if you want to import common utilities or configurations:
from .utils import load_config
from .storage import save_to_cassandra

# If you have any package-level setup or initialization, you can do it here.
# For example, you might initialize a logger or set some global variables.
# For this project, it can be left empty or very minimal.

# Example of a simple initialization (if needed):
# import logging
# logging.basicConfig(level=logging.INFO)