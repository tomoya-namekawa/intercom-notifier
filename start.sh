#!/bin/bash
set -ex

SCRIPT_DIR=$(cd "$(dirname "$0")" || exit; pwd)
cd "${SCRIPT_DIR}" || exit

. venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

source .env
exec python ./src/main.py
