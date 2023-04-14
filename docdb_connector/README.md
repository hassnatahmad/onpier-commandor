## Run a python pod
    kubectl run --rm -ti -n default python3-11 --image=python:3.11-slim /bin/bash
    mkdir app && cd app

## in another terminal
    kubectl cp src python3-11:/app/src && kubectl cp requirements-base.in python3-11:/app/requirements-base.in
    kubectl port-forward python3-11 8081:8081

## Run inside pod
    python -m venv venv && source venv/bin/activate && pip install -r requirements-base.in
    export PYTHONPATH=src:$PYTHONPATH
    export MONGO_DATABASE_URI=mongodb://<DB_USERNAME>:<DB_PASSWORD>@<ClusterName>.eu-central-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=/app/rds-combined-ca-bundle.pem&retryWrites=false
    python src/run.py
