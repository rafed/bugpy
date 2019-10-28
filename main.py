import os
import re
from git import Repo 

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

regexes = [
    # bug number
    'bug[# \t]*[0-9]+',
    'pr[# \t]*[0-9]+',
    'show\_bug\.cgi\?id=[0-9]+',
    '\[[0-9]+\]',
    # plain number
    '[0-9]+',
    # keyword
    'fix(e[ds])?|bugs?|defects?|patch',
]

# str = "afxaaasda you"
# x = re.search("fix(e[ds])?|bugs?|defects?|patch", str)
# print(x.pos)

def print_commit(commit):
    print('----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str("count: {} and size: {}".format(commit.count(), commit.size)))

repo = Repo('./RxJava/')
commits = list(repo.iter_commits('3.x'))

# repo = Repo('../rafed123.github.io')
# commits = list(repo.iter_commits())

# for c in commits:
#     print_commit(c)

# changedFiles = [ item.a_path for item in repo.index.diff(None) ]
# print(changedFiles)

# print(len(commits))

for commit in commits[:1000]:
    changed_files = []

    if commit.parents is (): continue
    commit_diff = commit.diff(commit.parents[0])

    print(commit.stats.files)

    # print(len(commit_diff))
    for diff in commit_diff:
        if diff.a_blob is None: continue

        # if diff.a_blob.path.endswith('.java'):
        #     file_contents = repo.git.show('{}:{}'.format(commit.hexsha, diff.a_blob.path))
        #     print(file_contents)

        print(diff.a_blob.path)

        # if diff.a_blob.path not in changed_files:
            # changed_files.append(diff.a_blob.path)
            
    #     if diff.b_blob is not None and diff.b_blob.path not in changed_files:
    #         changed_files.append(diff.b_blob.path)

        # print(diff.a_blob.path)
            
    # print((changed_files))
    print('###############')