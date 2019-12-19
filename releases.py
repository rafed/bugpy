import requests
import json

tags = []

# https://api.github.com/repos/tesseract-ocr/tesseract/tags

for i in range (1, 3): 
    print("Doing", i)

    url = "https://api.github.com/repositories/22887094/tags?page={}".format(i)

    r = requests.get(url)
    tag_page = json.loads(r.text)
    for data in tag_page:
        tags.append(data)


for tag in tags:
    print("{},{}".format(tag["name"], tag["commit"]["sha"]))

print(len(tags))