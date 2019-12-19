import requests
import json

tags = []

for i in range (1, 4): # 24
    print("Doing", i)

    url = "https://api.github.com/repositories/5108051/tags?page={}".format(i)

    r = requests.get(url)
    tag_page = json.loads(r.text)
    for data in tag_page:
        tags.append(data)


for tag in tags:
    print("{},{}".format(tag["name"], tag["commit"]["sha"]))

print(len(tags))
# print(json.dumps(tags, indent=2))
# print(len(tags))

# with open('data.txt', 'w') as outfile:
#     json.dump(issues, outfile)