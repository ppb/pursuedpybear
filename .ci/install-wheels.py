import glob
import io
import os
import subprocess
from urllib.request import urlopen
import zipfile

CIRRUS_BUILD_ID = os.environ['CIRRUS_BUILD_ID']
ARTIFACTS_URL = "https://api.cirrus-ci.com/v1/artifact/build/{}/build/dist.zip".format(CIRRUS_BUILD_ID)

with urlopen(ARTIFACTS_URL) as resp:
    zipdata = resp.read()

with zipfile.ZipFile(io.BytesIO(zipdata)) as zf:
    zf.extractall()

subprocess.run(
    ['pip', 'install', *glob.glob('dist/*.whl')],
    check=True
)
