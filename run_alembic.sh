#!/bin/bash
# Script to run alembic with .env loaded

# Load .env file
export $(grep -v '^#' .env | xargs)

# Run alembic command
alembic "$@"
