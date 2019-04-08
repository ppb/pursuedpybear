# PyPI Upload Scripts

I constantly have to lookup how to do the varying steps for this, so I
wrote some bash scripts for handling the artifact generation and PyPI
uploads, including to the test server.

## Process

1. Navigate to the directory root.
2. `sh ./.upload-scripts/env-build.sh`
3. `source ./.upload-venv/bin/activate`
4. `sh ./.upload-scripts/generate.sh`
5. Check the new build artifact for errors.
6. `sh ./.upload-scripts/test-upload.sh`
7. Check the uploaded version. Test install with
   `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ppb`
   When you're sure, move on.
8. `sh ./.upload-scripts/up`