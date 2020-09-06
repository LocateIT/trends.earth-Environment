#!/bin/bash
set -e

echo "Running script"
echo -e "$EE_PRIVATE_KEY" | base64 -d > service_account.json
exec /opt/conda/envs/env/bin/python main.py $1
