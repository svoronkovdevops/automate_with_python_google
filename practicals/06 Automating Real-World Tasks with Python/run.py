#!/usr/bin/env python3

import os
import requests

#Path to the data
path = "/data/feedback/"

keys = ["title", "name", "date", "feedback"]

folder = os.listdir(path)
for file in folder:
    key_count = 0
    feedback = {}
    with open(path + file) as fl:
        for line in fl:
            value = line.strip()
            feedback[keys[key_count]] = value
            key_count += 1
    print(feedback)
    reponse = requests.post("http://34.30.128.189/feedback/",json=feedback)
print(response.request.body)
print(response.status_code)