#! /usr/bin/env bash


# Let the DB start
python app/testing/db_start_test.py


# Run migrations
alembic upgrade head


# Create initial data in DB
python app/testing/initial_db.py