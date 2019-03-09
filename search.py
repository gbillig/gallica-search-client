import json
import os
import time

ark_database_filename = 'ark.json'
date_database_filename = 'date.json'

with open(ark_database_filename, 'rb') as fp:
  ark_id_hash = json.load(fp)

with open(date_database_filename, 'rb') as fp:
  date_hash = json.load(fp)
