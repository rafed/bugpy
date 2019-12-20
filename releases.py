import requests
import json

tags = []

# https://api.github.com/repos/tesseract-ocr/tesseract/tags
# https://api.github.com/repositories/455600/tags

for i in range (1, 5): 
    print("Doing", i)

    url = "https://api.github.com/repositories/1093228/tags?page={}".format(i)

    r = requests.get(url)
    tag_page = json.loads(r.text)
    for data in tag_page:
        tags.append(data)


for tag in tags:
    print("{},{}".format(tag["name"], tag["commit"]["sha"]))

print(len(tags))