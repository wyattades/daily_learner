# Daily Learner

Track your daily activities and your daily mood. Using machine learning, derive which activities make you most content.

## Setup

This project requires that you download [web2py](http://www.web2py.com/init/default/download), then add this project to the `web2py` `applications` folder.

To set this project as `web2py`'s default, create a `routes.py` file in the `web2py` folder with the following content:
```python
default_application='daily_learner'

routes_onerror = [
    ('*/*', '/daily_learner/error/index')
]
```

## Development

Run `python web2py.py -a <password>` in the `web2py` folder to start the server, or run `bash start.sh` in this folder.

Then visit `localhost:8000` to view the Daily Learner website.

## Production

TBD
