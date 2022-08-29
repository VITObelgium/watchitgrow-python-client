import pytest as pytest

from wig import Wig


@pytest.mark.parametrize("env", ['dev', 'prod'])
def test_main_init(env):
    wig = Wig(env=env)
    assert wig._auth is not None
    assert wig._api is not None
