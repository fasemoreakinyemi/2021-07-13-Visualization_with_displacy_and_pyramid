#!/usr/bin/env sh
python3 ./livivo_sru/data/seed_database.py
pserve development.ini
