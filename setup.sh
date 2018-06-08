#!/bin/bash

set -e

pip2.7 install --user numpy sklearn keras theano

echo '
{
    "floatx": "float32",
    "epsilon": 1e-07,
    "image_data_format": "channels_last",
    "backend": "theano"
}
' > ~/.keras/keras.json

echo "
default_application='daily_learner'

routes_onerror = [
  ('*/*', '/daily_learner/error/index')
]

routes_in = [
  ('/admin/$anything', '/admin/$anything'),
  ('/$app/static/$anything', '/$app/static/$anything'),
  ('/$app/error/$anything', '/$app/error/$anything'),
  ('/$app/api/$anything', '/$app/api/$anything'),
  ('/$anything', '/daily_learner/default/$anything'),
]
routes_out = [ (x, y) for (y, x) in routes_in[-1:] ]
" > ../../routes.py

echo "
daily_learner setup completed successfully!
"

