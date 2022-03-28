from pathlib import Path

from npb.utils import get_config
from npb.npb import NPB


def upload(file_path: Path, zip_flag: bool = False, plain: bool = False, description: str = None, lifetime: int = -1):
    """Upload file to ppb server."""

    config = get_config()
    ppb_config = config['ppb_config']
    npb = NPB()
    npb.connect(nc_uri=ppb_config['NC_HTTP_PATH'], nc_user=ppb_config['NC_USER'],
                nc_password=ppb_config['NC_PASSWORD'], mongodb_uri=ppb_config['PPB_TARGET_HOST_DB_URI'])
    url = npb.upload_file(file_path, sender=config['other']['SENDER_NAME']).get_link()

    print(f"Uploaded to {url}")

    return url
