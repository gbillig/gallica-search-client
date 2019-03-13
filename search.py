import json
import os
import time

ark_database_filename = 'ark.json'
date_database_filename = 'date.json'

def load_data_from_file()
  with open(ark_database_filename, 'rb') as f:
    ark_id_hash = json.load(f)

  with open(date_database_filename, 'rb') as f:
    date_hash = json.load(f)
