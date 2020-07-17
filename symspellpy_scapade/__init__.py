"""
symspellpy - original code S-capade based on for creating symmetric candidate lookup for research
.. moduleauthor:: mmb L <mammothb@hotmail.com>
.. moduleauthor:: Wolf Garbe <wolf.garbe@faroo.com>

symspellpy_scapade
.. moduleauthor:: Robert Young <robert.young2@ucdconnect.ie>

"""
from .__version__ import (__title__, __description__, __version__,
                          __author__, __author_email__, __license__)

from . import editdistance
from . import helpers
from .symspellpy import SymSpell, Verbosity
