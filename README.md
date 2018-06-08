# Daily Learner

A webapp for entering arbitrary data in a way that's accessible to anyone. Easily perform analytics and predictions using machine learning.

## Setup

1. Install Python2.7
2. Download [web2py](http://www.web2py.com/init/default/download), then add this project to the `web2py/applications` folder. The project must be named `daily_learner`.
3. `$ bash setup.sh`

## Development

### Setup for Development

1. Install [node.js](https://nodejs.org/en/download/) version 8 and up
2. `$ npm install`

Run `$ npm run dev` to start the web2py server and live-compile Sass files.

Then visit `localhost:8000` to view the Daily Learner website.

## Production

To start a headless production server, go to the root `web2py` folder then run `python web2py.py -a <password>`.
