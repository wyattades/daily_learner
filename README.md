# Daily Learner

A webapp for entering arbitrary data in a way that's accessible to anyone. Easily perform analytics and predictions using machine learning.

## Setup

1. This project requires that you download [web2py](http://www.web2py.com/init/default/download), then add this project to the `web2py` `applications` folder.
2. Install Node version 8 and up
2. `$ npm install`
3. `$ npm install -g gulp-cli`

To set this project as `web2py`'s default, create a `routes.py` file in the `web2py` folder with the following content:
```python
default_application='daily_learner'

routes_onerror = [
    ('*/*', '/daily_learner/error/index')
]
```


## Development

Run `$ gulp dev` to start the web2py server and live-compile Sass files.

Then visit `localhost:8000` to view the Daily Learner website.

## Production

To start a headless production server, go to the root `web2py` folder then run `python web2py.py -a <password>`.
