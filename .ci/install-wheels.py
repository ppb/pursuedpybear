import glob
import io
import os
import ssl
import subprocess
from urllib.request import urlopen
import zipfile

CIRRUS_BUILD_ID = os.environ['CIRRUS_BUILD_ID']
ARTIFACTS_URL = "https://api.cirrus-ci.com/v1/artifact/build/{}/build/dist.zip".format(CIRRUS_BUILD_ID)

# Windows certificate validation fails. This is per PEP476
with urlopen(ARTIFACTS_URL, context=ssl._create_unverified_context()) as resp:
    zipdata = resp.read()

with zipfile.ZipFile(io.BytesIO(zipdata)) as zf:
    zf.extractall()

subprocess.run(
    ['pip', 'install'] + glob.glob('dist/*.whl'),
    check=True
)
