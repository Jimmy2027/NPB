# -*- coding: utf-8 -*-
import pytest


@pytest.mark.tox
def test_import():
    import npb
    from npb.upload_files import upload


if __name__ == '__main__':
    test_import()
