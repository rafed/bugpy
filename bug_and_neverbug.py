from pydriller import RepositoryMining, GitRepository
import re
import sys
import os
import json
from datetime import datetime

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

def is_buggy_commit(msg):
    x = re.search(keyword_regex, msg, flags=re.IGNORECASE)
    if x:
        return True
    return False

def main():
    repo_path = sys.argv[1]
    repo_branch = 'master'

    base_dir_not_bug = "data2/not_bug/{}".format(os.path.basename(os.path.normpath(repo_path)))
    base_dir_bug = "data2/bug/{}".format(os.path.basename(os.path.normpath(repo_path)))
    if not os.path.exists(base_dir_bug):
        os.makedirs(base_dir_bug)
    if not os.path.exists(base_dir_not_bug):
        os.makedirs(base_dir_not_bug)

    gitRepo = GitRepository(repo_path)
    commits = RepositoryMining(repo_path, only_in_branch=repo_branch).traverse_commits()

    all_files = gitRepo.files()
    counter = 0
    total_files = len(all_files)
    for file in all_files:
        counter += 1
        relative_path = os.path.relpath(file, repo_path) 
        print("[*] {}/{} {}".format(counter, total_files, relative_path))
        
        if not valid_source_file(file):
            continue

        gprepo = gitRepo.repo

        modifying_commits = gprepo.iter_commits('--all', paths=relative_path)

        buggy = False

        for commit in modifying_commits:
            print(commit.hexsha)
            if is_buggy_commit(commit.message):
                print(commit.message)
                buggy = True
                break

        file_name_to_write = "{}_{}".format(counter, os.path.basename(file))
        if buggy:
            file_path_to_write = os.path.join(base_dir_bug, file_name_to_write)
            shutil.copyfile(file, file_path_to_write)
        else:
            file_path_to_write = os.path.join(base_dir_not_bug, file_name_to_write)
            shutil.copyfile(file, file_path_to_write)
            
    print("All Done!")


if __name__ == "__main__":
    main()