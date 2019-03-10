import json


with open('ark.json', 'rb') as fp:
  ark_id_hash = json.load(fp)

with open('date.json', 'rb') as fp:
  date_hash = json.load(fp)

if False:
  for article in articles:
    if 'é' in article["date"]:
      article['date'] = article['date'].replace('é', 'e')

    if 'û' in article["date"]:
      article['date'] = article['date'].replace('û', 'u')


month_sub = {
  " janvier ": "-01-",
  " février ": "-02-",
  " fevrier ": "-02-",
  " mars ": "-03-",
  " avril ": "-04-",
  " mai ": "-05-",
  " juin ": "-06-",
  " juillet ": "-07-",
  " août ": "-08-",
  " aout ": "-08-",
  " septembre ": "-09-",
  " octobre ": "-10-",
  " novembre ": "-11-",
  " décembre ": "-12-",
  " decembre ": "-12-",
}

if False:
  for ark_id, date in date_hash.items():
    for month_spelled, month_numerical in month_sub.items():
      if month_spelled in date:
        
        date_hash[ark_id] = date.replace(month_spelled, month_numerical)
        break


for ark_id, date in date_hash.items():
  new_date = date[6:10] + '-' + date[3:5] + '-' + date[0:2]
  date_hash[ark_id] = new_date


with open('date_nice.json', 'w', encoding='utf8') as fp:
  json.dump(date_hash, fp, sort_keys=True, indent=4)

