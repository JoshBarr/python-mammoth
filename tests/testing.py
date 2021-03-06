import os

from nose.tools import nottest


@nottest
def test_path(path):
    this_dir = os.path.dirname(__file__)
    return os.path.join(this_dir, "test-data", path)
