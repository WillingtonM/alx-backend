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
    qry = request.query_string.decode('utf-8').split('&')
    qry_table = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        qry,
    ))
    if 'locale' in qry_table:
        if qry_table['locale'] in app.config["LANGUAGES"]:
            return qry_table['locale']
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """
        Render html template
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
