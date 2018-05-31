from gluon.custom_import import NATIVE_IMPORTER
import sys

Keras = NATIVE_IMPORTER('keras')
sys.modules['keras'] = Keras
