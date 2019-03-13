import html2text
import requests
import xml.etree.ElementTree as ET
import json
import os
import time
import progressbar
from datetime import datetime


METADATA_BASE_URL = 'https://gallica.bnf.fr/services/Issues?ark=ark:/12148/'
RAW_TEXT_BASE_URL = 'https://gallica.bnf.fr/ark:/12148/'
top_ark_id = 'cb34393339w'
ark_database_filename = 'ark.json'
date_database_filename = 'date.json'
text_dir = './text'
out_dir = './results'

articles = []
ark_id_hash = {}
date_hash = {}

def adjust_date(date):
  month_sub = {
    " janvier ": "-01-",
    " février ": "-02-",
    " mars ": "-03-",
    " avril ": "-04-",
    " mai ": "-05-",
    " juin ": "-06-",
    " juillet ": "-07-",
    " août ": "-08-",
    " septembre ": "-09-",
    " octobre ": "-10-",
    " novembre ": "-11-",
    " décembre ": "-12-",
  }
  
  new_date = date
  
  for month_spelled, month_numerical in month_sub.items():
      if month_spelled in date:
        new_date = date.replace(month_spelled, month_numerical)
        break

  day = new_date[0:2]
  month = new_date[3:5]
  year = new_date[6:10]
  new_date = year + '-' + month + '-' + day
  
  return new_date

def load_data():
  if not os.path.isfile(ark_database_filename) or not os.path.isfile(date_database_filename):
    r = requests.get(METADATA_BASE_URL + top_ark_id + '/date')
    year_root = ET.fromstring(r.text)
    years = [child.text for child in year_root]

    for year in years:
      r = requests.get(METADATA_BASE_URL + top_ark_id + '/date&date=' + year)
      article_root = ET.fromstring(r.text)
      
      for article_xml in article_root:
        ark_id = article_xml.attrib['ark']
        date = article_xml.text
        date = adjust_date(date)

        if len(date) != 10:
          continue

        if date in ark_id_hash:
          ark_id_hash[date].append(ark_id)
        else:
          ark_id_hash[date] = [ark_id]

        date_hash[ark_id] = date

    with open(ark_database_filename, 'w+', encoding='utf8') as f:
      json.dump(ark_id_hash, f, indent=4)

    with open(date_database_filename, 'w+', encoding='utf8') as f:
      json.dump(date_hash, f, sort_keys=True, indent=4)

  else:
    with open(ark_database_filename, 'rb') as f:
      ark_id_hash = json.load(f)

    with open(date_database_filename, 'rb') as f:
      date_hash = json.load(f)

  return ark_id_hash, date_hash


def search(search_text, start_date, end_date, date_hash):
  now = datetime.now()
  output_filepath = out_dir + '/' + search_text + '-' + now.strftime("%Y-%m-%d %H:%M") + '.txt'
  with open(output_filepath, 'w', encoding='utf8') as outfile:
    for ark_id, date in date_hash.items():
      parsed_date = datetime.strptime(date, '%Y-%m-%d')

      if parsed_date > start_date and parsed_date < end_date:
        filepath = text_dir + '/' + ark_id + '.txt'

        with open(filepath, 'r') as f:
          searchlines = f.readlines()

        for i, line in enumerate(searchlines):
            if search_text in line:
                outfile.write('Found ' + search_text + ' in line ' + str(i) + ' of ' + ark_id + ' (' + date + ')\n')
                outfile.write(RAW_TEXT_BASE_URL + ark_id + '/item.r=' + search_text + '\n')
                for l in searchlines[i:i+3]: outfile.write(l)
                outfile.write('\n')
  
  return

def main():
  ark_id_hash, date_hash = load_data()

  if not os.path.isdir(text_dir):
    os.mkdir(text_dir)

  if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

  for ark_id, date in progressbar.progressbar(date_hash.items()):
    filepath = text_dir + '/' + ark_id + '.txt'
    if not os.path.isfile(filepath):
      r = requests.get(RAW_TEXT_BASE_URL + ark_id + '.texteBrut')
      file_text = html2text.html2text(r.text)
      
      with open(text_dir + '/' + ark_id + '.txt', 'w+', encoding='utf8') as f:
        f.write(file_text)
  
  search_text = input('Enter search query: ')
  start_date = datetime.strptime(input('Enter start date (DD-MM-YYYY): '), '%d-%m-%Y')
  end_date = datetime.strptime(input('Enter end date (DD-MM-YYYY): '), '%d-%m-%Y')

  search(search_text, start_date, end_date, date_hash)
  

if __name__ == "__main__":
  main()



