#!/usr/bin/env python3
"""
    Flask app (Basic).
"""
import pytz
from flask_babel import Babel
from typing import Union, Dict
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
    loc = request.args.get('locale', '')
    if loc in app.config["LANGUAGES"]:
        return loc
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    header_loc = request.headers.get('locale', '')
    if header_loc in app.config["LANGUAGES"]:
        return header_loc
    return request.accept_languages.best_match(app.config["LANGUAGES"])


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
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
