#!/usr/bin/env python3
"""
    Flask app (Basic).
"""
from flask_babel import Babel
from flask import Flask, render_template


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


@app.route('/')
def get_index() -> str:
    """
        The home index.html page.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
