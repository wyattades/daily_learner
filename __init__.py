from gluon.custom_import import NATIVE_IMPORTER
import sys
import os

# Fix capitalization imcompatibility between Keras and web2py
Keras = NATIVE_IMPORTER('keras')
sys.modules['keras'] = Keras

# Set Keras background to theano
if Keras.backend.backend() != 'theano':
  os.environ['KERAS_BACKEND'] = 'theano'
  reload(Keras.backend)
  assert Keras.backend.backend() == 'theano'
