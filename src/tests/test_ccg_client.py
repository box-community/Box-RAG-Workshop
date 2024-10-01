from box_sdk_gen import BoxClient
from utils.box_client_ccg import (
    AppConfig,
    get_ccg_enterprise_client,
    get_ccg_user_client,
    whoami,
)


def test_get_ccg_enterprise_client():
    config = AppConfig()
    client = get_ccg_enterprise_client(config)
    assert client is not None
    user = whoami(client)
    assert user is not None
    assert user.id is not None


def test_get_ccg_user_client():
    config = AppConfig()
    client = get_ccg_user_client(config, config.ccg_user_id)
    assert client is not None
    user = whoami(client)
    assert user is not None
    assert user.id == config.ccg_user_id


def test_client_fixture(box_client_ccg: BoxClient):
    assert box_client_ccg is not None
    user = whoami(box_client_ccg)
    assert user is not None
    assert user.id is not None


def test_client_user_fixture(box_client_ccg_user: BoxClient):
    assert box_client_ccg_user is not None
    user = whoami(box_client_ccg_user)
    assert user is not None
    assert user.id is not None
