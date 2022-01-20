#!/usr/bin/xonsh
import io
import os
import sys
import tempfile
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import zipfile

$RAISE_SUBPROC_ERROR = True

ARTIFACTS_URL = f"https://api.cirrus-ci.com/v1/artifact/build/{$CIRRUS_BUILD_ID}/build/dist.zip"
PYPI_TEST_REPO = "https://test.pypi.org/legacy/"

PROJECT = os.getcwd()

with tempfile.TemporaryDirectory() as td:
    print("Bundling examples...")
    with zipfile.ZipFile(f"{td}/examples.zip", 'w', compression=zipfile.ZIP_LZMA) as examples:
        for name, _, files in os.walk('examples'):
            if '__pycache__' in name:
                continue
            examples.write(f'{PROJECT}/{name}', arcname=name)
            for fname in files:
                examples.write(f'{PROJECT}/{name}/{fname}', arcname=f"{name}/{fname}")

    cd @(td)

    print("Downloading artifacts...")
    with urlopen(ARTIFACTS_URL) as resp:
        zipdata = resp.read()

    with zipfile.ZipFile(io.BytesIO(zipdata)) as zf:
        # nl = zf.namelist()
        # print(f"Found {len(nl)} files from build:", *nl)
        zf.extractall()

    dists = [f for f in pg`**` if '+' not in f.name and f.name != 'examples.zip' and f.is_file()]

    if not dists:
        print("No uploadable dists found, skipping upload")
        sys.exit(0)
    else:
        print("Found dists:", *dists)

    print("Uploading to test repo...")

    twine upload --repository-url @(PYPI_TEST_REPO) --username __token__ --password $TWINE_TEST_TOKEN @(dists)

    print("")

    if 'CIRRUS_RELEASE' in ${...}:

        print("Uploading to GitHub...")
        for dist in dists + [pf"{td}/examples.zip"]:
            print(f"\t{dist.name}...")
            dest_url = f"https://uploads.github.com/repos/{$CIRRUS_REPO_FULL_NAME}/releases/{$CIRRUS_RELEASE}/assets?name={dist.name}"
            with dist.open('rb') as fobj:
                buff = fobj.read()
                try:
                    resp = urlopen(Request(
                        url=dest_url,
                        method='POST',
                        data=buff,
                        headers={
                            "Authorization": f"token {$GITHUB_TOKEN}",
                            "Content-Type": "application/octet-stream",
                        },
                    ))
                except HTTPError as exc:
                    print(f"Error {exc.code} ({exc.reason}) from {dest_url}")
                    print(exc.headers)
                    print(exc.read())
                    raise

        print("")

        print("Uploading to PyPI...")
        twine upload --username __token__ --password $TWINE_PROD_TOKEN @(dists)
