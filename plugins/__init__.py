# plugins/__init__.py

from .start import start_handler  # Assuming you have a start_handler function in start.py
from .help import help_handler    # Assuming you have a help_handler function in help.py

__all__ = ['start_handler', 'help_handler']  # Specifies what should be imported when using 'from plugins import *'
