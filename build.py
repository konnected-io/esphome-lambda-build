import os
import sys
import urllib.parse

from esphome.__main__ import run_esphome
from esphome.util import run_external_process
from urllib.request import urlretrieve

def handler(event, context):
    
    print(sys.path)
    print(sys.executable)
    print(os.environ.get("PYTHONEXEPATH", os.path.normpath(sys.executable)))

    # test if we can run esptool.py
    run_external_process("python3","/opt/python/bin/esptool.py","version")

    config_url = event['config_url']
    try:
      parsed_url = urllib.parse.urlparse(config_url)
    except ValueError as e:
       raise "not valid config file url"
    
    fname = parsed_url.path.split('/').pop()
    config_file_path = "/tmp/" + fname

    if parsed_url.scheme == 'https' or parsed_url.scheme == 'http':
       urlretrieve(parsed_url.geturl(), config_file_path)      

    # test running esphome
    run_esphome(['esphome', 'version'])
    
    # compile the firmware
    run_esphome(['esphome', '--verbose', 'compile', config_file_path])
