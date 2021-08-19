import os
import tempfile

import pytest

from webapp import create_app
from webapp.models import db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
        yield client

    os.close(db_fd)
    os.unlink(db_path)