import configparser
import os
import tempfile
from pathlib import Path
from typing import Set

IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
VIDEO_EXTENSIONS = {'mov', 'mp4'}
COMPRESSION_EXTENSIONS = {'zip', 'tar', 'gz'}

GIT_ICON_HTML = '<head><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css"><style type="text/css">.fa_custom {color: #000000;}</style></head><body><a href="https://github.com/Jimmy2027/PPB"><i class="fa fa-github fa-3x" style="float:right"></i></a></body>'


def get_config_path() -> Path:
    """Get the config path."""

    config_path = Path('~/.config/npb.ini').expanduser()
    assert config_path.exists(), f'Config file not found under {config_path}. ' \
                                 f'Please fill the example under config and move it to {config_path}.'

    return config_path


def get_config():
    """Read the config and return it as a configparser object."""
    config_path = get_config_path()
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def check_extension(filename: str, extension_list: Set[str]) -> bool:
    """
    Returns true if the file extension is found in the extension list.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extension_list


def get_unique_str(prefix: str = '') -> str:
    from datetime import datetime
    dateTimeObj = datetime.now()
    dateStr = dateTimeObj.strftime("%Y_%m_%d_%H_%M_%S_%f")
    if prefix:
        return '_'.join([prefix, dateStr])
    else:
        return dateStr


def maybe_getfrom_ppb(download_url: str, out_path: Path):
    """Download from ppb and extract to out_path if not already there."""
    filename = Path(download_url).stem
    if not out_path.exists():
        out_path.mkdir()
        log.info(f'{out_path} does not exist. Downloading...')
        with tempfile.TemporaryDirectory() as tmpdirname:
            wget_command = f'wget {download_url} -P {tmpdirname}/'
            log.info(f'Getting {download_url}.')
            os.system(wget_command)

            unzip_command = f'unzip {tmpdirname}/{filename + ".zip"} -d {out_path}/'
            os.system(unzip_command)
    else:
        log.info(f'{out_path} exists. Skipping...')


def zotero_upload(pdf_path: Path):
    """
    Upload input pdf file to zotero database.
    """
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.config/ppb.conf'))
    user_id = config.getint('zotero', 'userID')
    api_key = config['zotero']['api_key']
    zot = zotero.Zotero(user_id, 'user', api_key)

    log.info(f'Uploading {pdf_path} to zotero database.')

    zot.attachment_both([(pdf_path.name, str(pdf_path))])


if __name__ == '__main__':
    # maybe_getfrom_ppb('https://ppb.hendrikklug.xyz/4959123face8.zip', Path('~/polymnistmodels').expanduser())
    # zotero_upload(Path('/Users/Hendrik/Documents/master_4/MMNF_RepSeP/work_in_progress/work_in_progress.pdf'))
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.config/ppb.conf'))
    user_id = config.getint('zotero', 'userID')
    api_key = config['zotero']['api_key']
    zot = zotero.Zotero(user_id, 'user', api_key)

    collections = zot.collections()

    # items = zot.top(limit=1000)
    # # we've retrieved the latest five top-level items in our library
    # # we can print each item's item type and ID
    # for item in items:
    #     print(f"Title: {item['data']['title']}| Key: {item['data']['key']}")

    pdf_path = Path('/Users/Hendrik/Documents/master_4/MMNF_RepSeP/proposal.pdf')
    # / Users / Hendrik / Zotero / storage / UFJLUPV7
    text_path = Path('~/temp.txt').expanduser()
    assert pdf_path.exists()
    print(zot.attachment_simple([str(pdf_path)], parentid='MFCRQXMV'))
    # zot.attachment_simple([str(text_path)])
    # zot.attachment_simple([str(pdf_path)], parentid='2LCR59FI')
    # zot.attachment_both([('mypdf', str(pdf_path))])
