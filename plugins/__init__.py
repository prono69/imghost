# plugins/__init__.py

from .start import start_handler
from .help import help_handler
# Import any other plugin handlers here if you have them

__all__ = ['start_handler', 'help_handler']  # Specifies what should be imported when using 'from plugins import *'
