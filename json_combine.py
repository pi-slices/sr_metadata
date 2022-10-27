#!/usr/bin/env python3

"""
json_combine.py

Load set of JSON files in specified range, add the token ID
to the start of the JSON structure, then write everything to
one merged file.

Author: Pi-Slices - @pislices
Website: pislices.art
Created: October 25, 2022
"""

import json

result = []

for i in range(8584, 39581):
    try:
        with open(f'output/{i}.json', 'r') as f:
            data_file = json.loads(f.read())
            new_data = {"tokenid": str(i)}
            new_data.update(data_file)
            result.append(new_data)
    except:
        continue #accounts for files that don't exist

with open('merged_json.json', 'w') as outfile:
    json.dump(result, outfile, indent = 4)
