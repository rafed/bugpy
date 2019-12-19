from pydriller import RepositoryMining, GitRepository
import re
import sys
import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import pickle
import traceback

import shutil

keyword_regex = 'fix(e[ds])?|bugs?|defects?|patch|bug[# \t]*[0-9]+'

java = ["java"]
cpp = ["cpp", "c", "cc", "cxx", "c++"] #"h", "hh", "hxx", "hpp", "h++"]
allowed_extensions = cpp


def valid_source_file(path):
    file_extension = path.split('.')[-1]
    if file_extension.lower() in allowed_extensions:
        return True
    return False

def is_bugfix_commit(msg):
    x = re.search(keyword_regex, msg, flags=re.IGNORECASE)
    if x:
        return True
    return False

def main():
    repo_path = sys.argv[1]
    repo_branch = 'master'

    commits = RepositoryMining(repo_path, only_in_branch=repo_branch).traverse_commits()
    commits = [commit for commit in commits]

    gitRepo = GitRepository(repo_path)

    start_date = commits[0].committer_date + relativedelta(years=3)
    last_date = commits[-1].committer_date - relativedelta(years=3)

    bug_tracker = defaultdict(list)
    bug_tracker_pickle = "data3/{}.pickle".format(os.path.basename(os.path.normpath(repo_path)))

    # First index the buggy files
    if os.path.exists(bug_tracker_pickle):
        with open(bug_tracker_pickle, 'rb') as handle:
            bug_tracker = pickle.load(handle)
    else:
        for commit_index, commit in enumerate(commits):
            if not is_bugfix_commit(commit.msg):
                continue

            try:
                for m in commit.modifications:
                    if not valid_source_file(m.filename):
                        continue

                    bug_commit = gitRepo.get_commits_last_modified_lines(commit, m) ### uses SZZ
                    # if bug_commit == {}: continue

                    bug_start_index = 99999999999999999999
                    for _file in bug_commit:
                        for i, _commit in enumerate(commits[:commit_index]):
                            if _commit.hash in bug_commit[_file] \
                                and i<bug_start_index:
                                bug_start_index = i

                    for _commit in commits[bug_start_index:commit_index]:
                        bug_tracker[_commit.hash].append(m.filename)
            except Exception as e:
                print("[***]", e)
                print(traceback.format_exc())
                print("Continuing for next commits")

            print(len(bug_tracker.keys()))
        with open(bug_tracker_pickle, 'wb') as handle:
            pickle.dump(bug_tracker, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Copy the files
    with open('maj_versions/{}.hash'.format(os.path.basename(os.path.normpath(repo_path)))) as f:
        major_releases = []
        for line in f.read().splitlines():
            tag,hash = line.split(',')
            major_releases.append((tag,hash))
        
    for version, commit in enumerate(commits):
        if not commit.hash in [item[1] for item in major_releases]:
            continue

        if commit.committer_date < start_date or commit.committer_date > last_date:
            continue

        for tag,hash in major_releases:
            if hash == commit.hash:
                break

        print("[*] Doing {}".format(tag))
        gitRepo.checkout(commit.hash)

        base_dir_not_bug = "data3/{}/{}/not_bug".format(os.path.basename(os.path.normpath(repo_path)), tag)
        base_dir_bug = "data3/{}/{}/bug".format(os.path.basename(os.path.normpath(repo_path)), tag)
        if not os.path.exists(base_dir_bug):
            os.makedirs(base_dir_bug)
        if not os.path.exists(base_dir_not_bug):
            os.makedirs(base_dir_not_bug)

        all_files = gitRepo.files()

        for _file in all_files:
            if not valid_source_file(_file):
                continue

            filename = os.path.basename(os.path.normpath(_file))
            if commit.hash in bug_tracker and filename in bug_tracker[commit.hash]:
                file_path_to_write = os.path.join(base_dir_bug, filename)
            else:
                file_path_to_write = os.path.join(base_dir_not_bug, filename)
                
            shutil.copyfile(_file, file_path_to_write)

    print("All Done!")


if __name__ == "__main__":
    main()