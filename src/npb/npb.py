import xml.etree.ElementTree as ET
from pathlib import Path

import six
from modun.BaseMongodbClass import BaseMongodbClass
from owncloud import Client, HTTPResponseError, ShareInfo


class MyOwnCloud(Client):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)

    def share_file_with_link(self, path, **kwargs):
        """Shares a remote file with link

        Modified version that fixes #263

        :param path: path to the remote file to share
        :param perms (optional): permission of the shared object
        defaults to read only (1)
        :param public_upload (optional): allows users to upload files or folders
        :param password (optional): sets a password
        http://doc.owncloud.org/server/6.0/admin_manual/sharing_api/index.html
        :param name (optional): display name for the link
        :returns: instance of :class:`ShareInfo` with the share info
            or False if the operation failed
        :raises: HTTPResponseError in case an HTTP error status was returned
        """
        perms = kwargs.get('perms', None)
        public_upload = kwargs.get('public_upload', 'false')
        password = kwargs.get('password', None)
        name = kwargs.get('name', None)

        path = self._normalize_path(path)
        post_data = {
            'shareType': self.OCS_SHARE_TYPE_LINK,
            'path': self._encode_string(path),
        }
        if (public_upload is not None) and (isinstance(public_upload, bool)):
            post_data['publicUpload'] = str(public_upload).lower()
        if isinstance(password, six.string_types):
            post_data['password'] = password
        if name is not None:
            post_data['name'] = self._encode_string(name)
        if perms:
            post_data['permissions'] = perms

        res = self._make_ocs_request(
            'POST',
            self.OCS_SERVICE_SHARE,
            'shares',
            data=post_data
        )
        if res.status_code == 200:
            tree = ET.fromstring(res.content)
            self._check_ocs_status(tree)
            data_el = tree.find('data')
            return ShareInfo(
                {
                    'id': data_el.find('id').text,
                    'path': path,
                    'url': data_el.find('url').text,
                    'token': data_el.find('token').text,
                    'name': data_el.find('name').text if 'name' in data_el else ''
                }
            )
        raise HTTPResponseError(res)


class NPB(BaseMongodbClass):
    def __init__(self):
        super().__init__()

    def connect(self, nc_uri, nc_user, nc_password, mongodb_uri):
        self.connect_nc(nc_uri, nc_user, nc_password)

    def connect_nc(self, nc_uri, nc_user, nc_password):
        self.oc = MyOwnCloud(nc_uri)
        self.oc.login(nc_user, nc_password)

    def upload_file(self, file_path: Path, sender: str) -> str:
        nc_fn = f'npb/{file_path.name}'
        self.oc.put_file(local_source_file=file_path,
                         remote_path=nc_fn)
        return self.oc.share_file_with_link(nc_fn)
