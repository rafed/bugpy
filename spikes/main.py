import os
import re
import difflib
import shutil
from git import Repo 

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

bug_regexes = [
    'bug[# \t]*[0-9]+',
    'pr[# \t]*[0-9]+',
    'show\_bug\.cgi\?id=[0-9]+',
    '\[[0-9]+\]'
]

plain_number_regex = '[0-9]+'
keyword_regex = 'fix(e[ds])?|bugs?|defects?|patch'

def syntactic_analysis(text):
    has_bug_number = False
    has_keyword = False
    has_plain_num = False
    
    for r in bug_regexes:
        x = re.search(r, text)
        if x:
            has_bug_number = True
            break

    # x = re.search(plain_number_regex, text)
    # if x:
    #     has_plain_num = True

    x = re.search(keyword_regex, text)
    if x:
        has_keyword = True

    # syn = 0
    # if has_bug_number:
    #     syn += 1

    # if has_keyword or ((has_plain_num and not has_bug_number) or (not has_plain_num and has_bug_number)):
    #     syn += 1

    if has_keyword:
        return 1
    return 0

def print_commit(commit):
    print('----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str("count: {} and size: {}".format(commit.count(), commit.size)))


def main():
    repo = Repo('./RxJava/')
    commits = list(repo.iter_commits('3.x'))

    for commit in commits[:1000]:
        changed_files = []

        if commit.parents is (): continue # workaround for some buggy behavior
        commit_diff = commit.diff(commit.parents[0]).iter_change_type('M')

        # print(repo.git.diff)
        # break

        # print(commit.stats.files)
        a = syntactic_analysis(commit.summary)
        if a>0:
            print(commit.summary, a)

            # for diff in commit_diff:
            #     if diff.a_blob is None: continue

            #     s = difflib.ndiff(diff.a_blob.data_stream.read().decode('utf-8'), diff.b_blob.data_stream.read().decode('utf-8'))
            #     print(s)

                # if diff.a_blob.path.endswith('.java'):
                #     file_contents = repo.git.show('{}:{}'.format(commit.hexsha, diff.a_blob.path))
                #     print(file_contents)

                # print("\t", diff.a_blob.path)
                # print('LA\t', diff.a_blob.path)

                # print(diff.a_blob.data_stream.read().decode('utf-8'))
                # print(diff.b_blob.data_stream.read().decode('utf-8'))

                # if diff.a_blob.path not in changed_files:
                #     changed_files.append(diff.a_blob.path)
                    
                # if diff.b_blob is not None and diff.b_blob.path not in changed_files:
                #     changed_files.append(diff.b_blob.path)

                    
            # print(changed_files)
            # print('###############')
            # break
        # shutil.copyfile(accepted_file, os.path.join(dest_patched,str(i)+accepted_file_name))

if __name__ == "__main__":
    main()

gr.checkout('a7053a4dcd627f5f4f213dc9aa002eb1caf926f8')