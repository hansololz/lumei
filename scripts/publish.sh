#!/bin/bash
python3 -m build
twine upload --skip-existing dist/*