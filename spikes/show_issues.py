import json

with open('data.txt', 'r') as myfile:
    data=myfile.read()

issues = json.loads(data)
# print(json.dumps(obj, indent=2))

for issue in issues:
    print(issue['title'])
    print(issue['number'])
    print(issue['assignees'])
    # print(json.dumps(issue, indent=2))
    # break
