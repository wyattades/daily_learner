from gluon.custom_import import NATIVE_IMPORTER
import sys

# Fix capitalization imcompatibility between Keras and web2py
Keras = NATIVE_IMPORTER('keras')
sys.modules['keras'] = Keras
