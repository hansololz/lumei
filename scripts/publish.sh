#!/bin/bash
rm -rf dist
python3 -m build
twine upload --skip-existing dist/*