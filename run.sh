#!/bin/bash
cat app/config_prod.yaml | envsubst > app/config.yaml

alembic upgrade head
python main.py