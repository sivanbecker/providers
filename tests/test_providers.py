import os
import pytest
from providers import __version__
import tempfile
from providers import providers


@pytest.fixture
def client():
    db_fd, providers.app.config['DATABASE'] = tempfile.mkstemp()
    providers.app.config['TESTING'] = True

    with providers.app.test_client() as client:
        with providers.app.app_context():
            providers.init_db()
        yield client

    os.close(db_fd)
    os.unlink(providers.app.config['DATABASE'])

def test_version():
    assert __version__ == '0.1.0'
