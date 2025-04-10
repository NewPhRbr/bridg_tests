import logging
from threading import Thread
from time import sleep

import pytest
from flask import Flask

from web.app import app as test_app


@pytest.fixture(scope="session")
def app():
    yield test_app


@pytest.fixture(scope="session")
def server(app: Flask):
    thread = Thread(target=app.run, daemon=True)
    thread.start()
    sleep(1)
