from pydriller import RepositoryMining, GitRepository
import re
import sys
import os
import json
from datetime import datetime
import pytz

utc=pytz.UTC

bug_regexes = [
    'bug[# \t]*[0-9]+',
    'pr[# \t]*[0-9]+',
    'show\_bug\.cgi\?id=[0-9]+',
    '\[[0-9]+\]'
]

plain_number_regex = '[0-9]+'
keyword_regex = 'fix(e[ds])?|bugs?|defects?|patch'

java = ["java"]
cpp = ["cpp", "c", "cc", "cxx", "c++", "h", "hh", "hxx", "hpp", "h++"]
allowed_extensions = cpp

def syntactic_analysis(text):
    x = re.search(keyword_regex, text, flags=re.IGNORECASE)
    if x:
        return True
    return False

def valid_modification(m):
    file_extension = m.filename.split('.')[-1]
            
    if file_extension.lower() not in allowed_extensions:
        return False

    if m.source_code == None:
        return False    

    return True

def valid_commit(commit):
    if not syntactic_analysis(commit.msg):
        return False
        # print(commit.msg.split('\n')[0], commit.hash)

    if len(commit.modifications) > 1:
        return False

    return True

def main():
    repo_path = sys.argv[1]
    repo_branch = 'master'
    base_dir_fixed = "data/fixed/{}".format(os.path.basename(os.path.normpath(repo_path)))
    base_dir_bug = "data/bug/{}".format(os.path.basename(os.path.normpath(repo_path)))
    os.makedirs(base_dir_bug)
    os.makedirs(base_dir_fixed)

    gitRepo = GitRepository(repo_path)
    commits = RepositoryMining(repo_path, only_in_branch=repo_branch).traverse_commits()

    i = 0

    for commit in commits:
        # print(commit.hash, commit.msg.split('\n')[0])
        if not valid_commit(commit):
            continue

        i+=1
        # if i==250: break

        fixed_files = []
        for m in commit.modifications:
            if not valid_modification(m):
                continue

            bug_commit = gitRepo.get_commits_last_modified_lines(commit, m) ### uses SZZ

            if bug_commit == {}:
                # print(bug_commit == {})
                continue

            fixed_files.append(m.filename)
            # fixed files
            fixed_file_name = "{}/{}_{}_{}".format(base_dir_fixed, str(i), commit.hash[:6], m.filename)
            # with open(fixed_file_name, 'w') as the_file:
            #     the_file.write(m.source_code)
            
            for file in bug_commit:
                if file.split('/')[-1] not in fixed_files:
                    continue
                # print("\tfalallala", file, fixed_files)

                latest_bug_commit_date = utc.localize(datetime.strptime("1/1/1950 00:00:00", "%d/%m/%Y %H:%M:%S"))
                latest_bug_commit_hash = ""

                for past_commit_hash in bug_commit[file]:
                    past_commit = gitRepo.get_commit(past_commit_hash)
                    past_commit_date = past_commit.committer_date.replace(tzinfo=utc)
                    if past_commit_date > latest_bug_commit_date:
                        latest_bug_commit_date = past_commit.author_date
                        latest_bug_commit_hash = past_commit_hash
                
                latest_bug_commit = gitRepo.get_commit(latest_bug_commit_hash)

                for bug_m in latest_bug_commit.modifications:
                    if bug_m.filename not in fixed_files:
                        continue

                    if bug_m.source_code == None:
                        continue

                    bug_file_name = "{}/{}_{}_{}".format(base_dir_bug, str(i), latest_bug_commit.hash[:6], bug_m.filename)
                    with open(bug_file_name, 'w') as the_file:
                        the_file.write(bug_m.source_code)

                    with open(fixed_file_name, 'w') as the_file:
                        the_file.write(m.source_code)

            print("********")
            # print(i)#, commit.msg)
            print(fixed_file_name)
            print(bug_file_name)

if __name__ == "__main__":
    main()