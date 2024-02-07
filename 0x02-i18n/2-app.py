#!/usr/bin/env python3
"""
    Flask app (Basic).
"""
from flask_babel import Babel
from flask import Flask, render_template, request


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


@babel.localeselector
def get_locale() -> str:
    """
        Gets locale from: request object
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """
        Render html template
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
