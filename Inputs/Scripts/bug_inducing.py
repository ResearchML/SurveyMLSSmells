import ast
import csv
import json
import os
from pydriller import GitRepository, RepositoryMining

from src.mouna.constants import bug_keywords

def run_main():
    # path = "/Users/mosesopenja/Documents/summer2020/Fork-Based Development/Dataset/Cloned";
    path = "/Users/mosesopenja/Documents/Winter2020/Mouna-Revised/clones";

    # path = Path("home/travail/downloads/")
    # projects = ["google/conscrypt","bytedeco/javacpp","sosy-lab/java-smt","tada/pljava","luben/zstd-jni","jpype-project/jpype","realm/realm-java","facebook/rocksdb","videolan/vlc-android"]
    # projects = ["google/conscrypt","bytedeco/javacpp","sosy-lab/java-smt","tada/pljava","luben/zstd-jni","jpype-project/jpype","realm/realm-java","facebook/rocksdb","videolan/vlc-android"]

    # projects = ["frostwire/frostwire"]

    # projectList = ["rocksdb","realm-java","jpype","pljava", "javacpp","conscrypt", "zstd-jni","vlc-android"]
    # projectList = ["photoprism","transformers","DeepSpeech"]
    projectList = ["vlc-android", "java-smt"]
    for project in projectList:
        # project_path = "{}/{}".format(path, project)
        # split = project.split("/")[1]
        # clone(path,project)
        fullPath = "{}/{}".format(path, project)

        data_file = open('{}/bug-detals-{}.csv'.format(path, project), mode='w', newline='', encoding='utf-8')
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(
            ['project', 'Bugfixing', "Name", "Email", "Date", "Bugs", "Commit-message", "", "Total-BugInducing",
             'Bug-Inducing'])
        data_writer.writerow([project, '', "", "", "", "", "", "", "", ''])

        data_file2 = open('{}/bug-detals-{}-summery.csv'.format(path, project), mode='w', newline='', encoding='utf-8')
        data_writer2 = csv.writer(data_file2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer2.writerow(
            ['project', "Total-Commits", 'Bugfixing', "Total-BugInducing", "Total-Added", "Total-Deleted",
             "Added-BugFixing", "Deleted-Bugfixing"])

        gr = GitRepository(os.path.abspath(fullPath))
        total_buggy_commits = 0
        total_inducing_commits = 0
        total_added = 0
        total_deleted = 0

        added_buggy = 0
        deleted_buggy = 0
        index = 0
        for commit in RepositoryMining(os.path.abspath(fullPath)).traverse_commits():
            print("{} : {}".format(index, commit.hash))
            index += 1
            flag = 0
            bug_msg = ""
            added = 0
            deleted = 0
            try:
                for modified in commit.modifications:
                    added += modified.added
                    deleted += modified.removed
                total_added += added
                total_deleted += deleted
                for bug in bug_keywords:
                    if bug in commit.msg.lower():
                        flag = 1
                        bug_msg = "{}{} , ".format(bug_msg, bug)
                        added_buggy += added
                        deleted_buggy += deleted
                if flag == 1:
                    total_buggy_commits += 1
                    buggy_commits = gr.get_commits_last_modified_lines(commit)
                    inducing_commits = 0
                    inducing_commits += len(buggy_commits)
                    items = buggy_commits.items()
                    buggy_string = ""
                    for key in buggy_commits.keys():
                        buggy = "{}:".format(key)
                        data = str(buggy_commits.get(key))
                        data2 = data.replace("\'", "\"")
                        # print(json.dump(buggy_commits.get(key)))
                        res = ast.literal_eval(data2)
                        for val in res:
                            hash_val = val
                            buggy = "{}{},".format(buggy, hash_val)
                        buggy_string = "{}{}XXXXXXX".format(buggy_string, buggy)
                    data_writer.writerow(
                        ['', commit.hash, commit.author.name, commit.author.email, commit.author_date, bug_msg,
                         commit.msg, "", '{}'.format(inducing_commits), '{}'.format(buggy_string)])
                    print("{} : {} - {}".format(total_buggy_commits, commit.hash, buggy_string))
                    total_inducing_commits += inducing_commits
            except:
                print("OPP... Error occured")
                pass

        data_writer2.writerow(
            [project, '{}'.format(index), '{}'.format(total_buggy_commits), '{}'.format(total_inducing_commits),
             '{}'.format(total_added), '{}'.format(total_deleted), '{}'.format(added_buggy),
             '{}'.format(deleted_buggy)])
        data_file.close()
        data_file2.close()

if __name__ == '__main__':
    run_main()

