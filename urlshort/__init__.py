from flask import Flask

def create_app(test_config=None):
    # create a flask app, "__name__" is the name of the module which is currently running in the Flask, basically the name of this file
    app = Flask(__name__)
    # in real case, should be a random key generated to encrypt the message
    app.secret_key = "frneirv3nFGHc68jwnew45erfdSW"

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app