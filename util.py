import json


with open('articles.json', 'rb') as fp:
  articles = json.load(fp)

for article in articles:
  if 'é' in article["date"]:
    article['date'] = article['date'].replace('é', 'e')

  if 'û' in article["date"]:
    article['date'] = article['date'].replace('û', 'u')

with open('articles_nice.json', 'w', encoding='utf8') as fp:
  json.dump(articles, fp, sort_keys=True, indent=4)

