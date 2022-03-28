# NPB - The Personal Pastebin for Nextcloud

A simple and emerging script allowing you to pastebin files and terminal output to a webserver to which you have SSH access.

## Rationale

With pastebins becoming increasingly cluttered with ads and eye candy as well as increasingly restrictive in terms of file size and temporal persistency, it seems you need to take things into your own hands!
PPB, the Personal PasteBin is a simple script allowing you to quickly upload and share files on your machine.

## Usage
Fill the template config file under `config` and move it to `~/.config/ppb.conf`
```console
user@host $ ppb -h                                                                                                                                                                                                                               (base) 
usage: ppb [-h] [--zip_flag] file

positional arguments:
  file                  file to upload and display

optional arguments:
  -h, --help            show this help message and exit
  --zip_flag, -zip_flag
                        zip folder and upload it. The folder to be zipped
                        needs to be after the flag -z. Example: ppb -z test

user@host $ ppb somefile.png
sending incremental file list
somefile.png
        223,298 100%  181.70MB/s    0:00:00 (xfr#1, to-chk=0/1)

sent 223,450 bytes  received 35 bytes  148,990.00 bytes/sec
total size is 223,298  speedup is 1.00
Uploaded to: https://some.url/ppb/bb04fc.png

user@host $ ppb -z somefolder
sending incremental file list
building file list ... 
ceee466acaa5.zip
         108 100%    0.00kB/s    0:00:00 (xfer#1, to-check=0/1)

sent 220,350 bytes  received 20 bytes  148,850.00 bytes/sec
total size is 220,300  speedup is 1.00
Uploaded to: https://some.url/ppb/ceee466acaa5.zip
```

## Installation
### As a user
```
pip install git+https://github.com/Jimmy2027/PPB.git
```

### As a host, using an Apache webserver
```
mkdir /var/www/ppb
cp ~/src/ppb/ppb.wsgi /var/www/ppb/
```
create a new virtual host:
```
<VirtualHost *:5001>
    ServerName localhost

    WSGIDaemonProcess ppb user=apache group=apache threads=2
    WSGIScriptAlias / /var/www/ppb/ppb.wsgi

    ErrorLog /var/log/apache2/ppb_error.log
    CustomLog /var/log/apache2/ppb_access.log combined

    <Directory /var/www/ppb>
        WSGIProcessGroup ppb
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
```

## Further Development

Currently the software is very minimal.
Help is appreciated in extending it!
