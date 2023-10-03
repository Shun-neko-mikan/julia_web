#!/usr/bin/env bash
# exit on error
set -o errexit

/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip

pip install -r requirements.txt

python ./satori/manage.py collectstatic --no-input
python ./satori/manage.py migrate
python ./satori/manage.py newsuperuser
