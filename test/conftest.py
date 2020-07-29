import pytest
import webtest as wt
import server
#  from ... import server
#  from ...server import create_server

@pytest.yield_fixture(scope='function')
def server():
    """An application for the tests."""
    _server = create_server()

    # I have no idea what these lines are doing
    ctx = _server.server.test_request_context()
    ctx.push()

    yield _server.server

    ctx.pop()
