# -*- coding: utf-8 -*-

# because Kenneth Reitz told me to do this:
# http://docs.python-guide.org/en/latest/writing/structure/#test-suite

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import c2xt
