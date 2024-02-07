#!/usr/bin/env python3
"""
    Flask app (Basic).
"""
import pytz
from typing import Union, Dict
from flask_babel import Babel, format_datetime
from flask import Flask, render_template, request, g


class Config:
    """
        Config class for the babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Instantiate application object
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

# Wrap application with Babel
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """
        Validate user login details using user id
        Args: id
        Returns: user dictionary if valid id else None
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """
        Adds valid user to global session object 'g'
    """
    usr = get_user()
    g.user = usr


@babel.localeselector
def get_locale() -> str:
    """
        Gets locale from: request object
    """
    queries = request.query_string.decode('utf-8').split('&')
    query_table = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        queries,
    ))
    loc = query_table.get('locale', '')
    if loc in app.config["LANGUAGES"]:
        return loc
    usr_info = getattr(g, 'user', None)
    if usr_info and usr_info['locale'] in app.config["LANGUAGES"]:
        return usr_info['locale']
    header_loc = request.headers.get('locale', '')
    if header_loc in app.config["LANGUAGES"]:
        return header_loc
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone() -> str:
    """
        Gets timezone from request object
    """
    time_zn = request.args.get('timezone', '').strip()
    if not time_zn and g.user:
        time_zn = g.user['timezone']
    try:
        return pytz.timezone(time_zn).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def get_index() -> str:
    """
        Render html template
    """
    g.time = format_datetime()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
