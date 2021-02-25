#!/bin/bash
cat app/config_prod.yaml | envsubst > app/config.yaml
export PYTHONPATH=$PYTHONPATH:.
pip install python-dateutil==2.8.1
alembic upgrade head
python main.py