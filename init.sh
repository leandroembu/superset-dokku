#!/usr/bin/env bash

# create an admin user
superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email $SUPERSET_ADMIN_EMAIL \
  --password $SUPERSET_ADMIN_PASSWORD

# Migrate DB to latest
superset db upgrade

# Setup roles
superset init

# Start server
superset run -p $PORT --with-threads --reload --debugger --host=0.0.0.0
