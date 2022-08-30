import pytest as pytest

from pywig import Wig


@pytest.mark.parametrize("env", ['prod'])
def test_main_init(env):
    wig = Wig(env=env)
    assert wig._auth is not None
    assert wig._api is not None
