from .Keras_BlackBox_Model import BlackBoxModel
from .Keras_Linear_Model import LinearModel
from .Scikit_Model import ScikitModel
from .Exceptions import *

MODELS = {
  'BlackBoxModel': BlackBoxModel,
  'LinearModel': LinearModel,
  'ScikitModel': ScikitModel,
}

def rows_to_dataframe(rows, labels):
  return [ [ row[label] for label in labels ] for row in rows ]
