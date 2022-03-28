# -*- coding: utf-8 -*-
import os
from pathlib import Path

from npb.upload_files import upload


def test_upload():
    test_file = Path(__file__).parent / 'test_file.txt'
    upload(file_path=test_file)


def test_cli_upload():
    os.system('npb test_file.txt')


if __name__ == '__main__':
    test_upload()
    # test_cli_upload()
