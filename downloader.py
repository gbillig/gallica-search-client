import html2text
import requests
import xml.etree.ElementTree as ET
import json
import os
import time
import progressbar


METADATA_BASE_URL = 'https://gallica.bnf.fr/services/Issues?ark=ark:/12148/'
RAW_TEXT_BASE_URL = 'https://gallica.bnf.fr/ark:/12148/'
top_ark_id = 'cb34393339w'
ark_database_filename = 'ark.json'
date_database_filename = 'date.json'
text_dir = './text'

articles = []
ark_id_hash = {}
date_hash = {}

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

      for month_spelled, month_numerical in month_sub.items():
        if month_spelled in date:
          date = date.replace(month_spelled, month_numerical)
          break

      if date in ark_id_hash:
        ark_id_hash[date].append(ark_id)
      else:
        ark_id_hash[date] = [ark_id]

      date_hash[ark_id] = date

  with open(ark_database_filename, 'w+', encoding='utf8') as fp:
    json.dump(ark_id_hash, fp, indent=4)

  with open(date_database_filename, 'w+', encoding='utf8') as fp:
    json.dump(date_hash, fp, sort_keys=True, indent=4)

else:
  with open(ark_database_filename, 'rb') as fp:
    ark_id_hash = json.load(fp)

  with open(date_database_filename, 'rb') as fp:
    date_hash = json.load(fp)

print(len(date_hash))
print(len(ark_id_hash))

if not os.path.isdir(text_dir):
  os.mkdir(text_dir)

for ark_id, date in progressbar.progressbar(date_hash.items()):
  r = requests.get(RAW_TEXT_BASE_URL + ark_id + '.texteBrut')
  file_text = html2text.html2text(r.text)
  
  with open(text_dir + '/' + ark_id + '.txt', 'w+', encoding='utf8') as fp:
    fp.write(file_text)
 

  



