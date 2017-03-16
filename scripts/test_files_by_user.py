import random

from dmp import dmp

users = ["adam", "ben", "chris", "denis", "eric"]

da = dmp(test=True)

for u in users:
    results = da.get_files_by_user(u)
    print(u, len(results))