import requests
import json

state = "all"
labels = "bug"

issues = []

for i in range (1, 4): # 24
    print("Doing", i)

    url = "https://api.github.com/repos/ReactiveX/RxJava/issues?state={}&labels={}&page={}".format(state, labels, i)

    r = requests.get(url)
    issue_page = json.loads(r.text)
    for iss in issue_page:
        issues.append(iss)

# data = json.loads(issues)

print(json.dumps(issues, indent=2))
print(len(issues))

with open('data.txt', 'w') as outfile:
    json.dump(issues, outfile)

    # for issue in issues:
    #     print(issue['title'])
    #     for label in issue['labels']:
    #         print("\t", label['name'])
    #         # if "bug" in label['name']:
    #         #     print(issue)


    # print(len(issues))