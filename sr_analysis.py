#!/usr/bin/env python3

"""
sr_analysis.py

The following script produces several statistics from the metadata of SuperRare v2 Tokens.

The metadata JSON file was compiled by individually downloading the 'tokenURI' contents
of each token on SuperRare's contract found at 0xb932a70A57673d89f4acfFBE830E8ed7f75Fb9e0.

Each metadata file was then combined into one large JSON file,
with the addition of each token's tokenID.

All analysis in the current iteration of this script was performed on token IDs 8584 to 39581,
as earlier tokens are missing the 'media' metadata.

---

Author: Pi-Slices - @pislices
Website: pislices.art
Created: October 24, 2022

"""

import json
import statistics
from collections import Counter

def load_json():
    """
    Load the JSON file containing all SuperRare token metadata.
    """
    with open('merged_json.json', 'r') as file:
        return json.load(file)

def mimetype_info(data):
    """
    Calculate the average/median filesize, and count of each mimeType SR supports.

    Args:
        data: JSON metadata.
    """
    mime_dict = {
        'image/png': [],
        'image/jpeg': [],
        'image/gif': [],
        'image/apng': [],
        'video/mp4': [],
        'video/webm': [],
        'model/gltf-binary': [],
        'image/svg+xml': [],
        '': []
    }

    for prop in data:
        if 'media' in prop:
            mime = prop['media']['mimeType']
            size = int(prop['media']['size'])

            mime_dict[mime].append(size)

    print(f"mimeType {'':^8} | avg size | count {'':^6} | median size")
    print('-'*55)
    for key in mime_dict:
        if len(mime_dict[key]) == 0:
            continue
        mean = statistics.mean(mime_dict[key]) / (1<<20)
        median = statistics.median(map(float, mime_dict[key]))/(1<<20)
        length = len(mime_dict[key])
        print(f"{key:17} | {mean:^5,.2f} MB | {length:>5} tokens | {median:,.2f} MB")


def size_info(data):
    """
    Count the number of mp4 files with file sizes in each 10 MB increment from 0-50 MB.

    Args:
        data: JSON metadata.
    """
    size_dict = {
        '0 - 10 MB': [],
        '10 - 20 MB': [],
        '20 - 30 MB': [],
        '30 - 40 MB': [],
        '40 - 50 MB': []
    }

    for prop in data:
        if 'media' in prop:
            mime = prop['media']['mimeType']
            size = int(prop['media']['size'])

            if mime == "video/mp4":
                if 0 <= size < 10485760:
                    size_dict['0 - 10 MB'].append(size)
                elif 10485760 <= size < 20971520:
                    size_dict['10 - 20 MB'].append(size)
                elif 20971520 <= size < 31457280:
                    size_dict['20 - 30 MB'].append(size)
                elif 31457280 <= size < 41943040:
                    size_dict['30 - 40 MB'].append(size)
                else:
                    size_dict['40 - 50 MB'].append(size)

    print("Range of video/mp4 filesizes:")
    for key in size_dict:
        print(f"{key}, {len(size_dict[key])} tokens")


def large_size_trend(data):
    """
    Count the number of mp4 files with file sizes above 40 MB, split into ~5000 token increments.

    Args:
        data: JSON metadata.
    """
    id_dict = {
        '8584 - 13000': [],
        '13001 - 18000': [],
        '18001 - 23000': [],
        '23001 - 28000': [],
        '28001 - 33000': [],
        '33001 - 39581': []
    }

    size_min = 41943040 #40 MB in Bytes

    for prop in data:
        if 'media' in prop:
            mime = prop['media']['mimeType']
            size = int(prop['media']['size'])
            tokenid = int(prop['tokenid'])

            if mime == "video/mp4" and tokenid in range(8584,39581) and size >= size_min:
                if 8584 <= tokenid <= 13000:
                    id_dict['8584 - 13000'].append(tokenid)
                elif 13001 <= tokenid <= 18000:
                    id_dict['13001 - 18000'].append(tokenid)
                elif 18001 <= tokenid <= 23000:
                    id_dict['18001 - 23000'].append(tokenid)
                elif 23001 <= tokenid <= 28000:
                    id_dict['23001 - 28000'].append(tokenid)
                elif 28001 <= tokenid <= 33000:
                    id_dict['28001 - 33000'].append(tokenid)
                else:
                    id_dict['33001 - 39581'].append(tokenid)

    print("Trend of >=40 MB mp4 files over time:")
    for key in id_dict:
        print(f"IDs: {key}: {len(id_dict[key])} tokens")

def largest_file(data):
    """
    Finds the token with the largest filesize on SuperRare.

    Args:
        data: JSON metadata.
    """
    #Initial placeholders for comparison
    size = 0
    largest = 0
    lrg_id = None

    for prop in data:
        if 'media' in prop:
            size = int(prop['media']['size'])
            if size > largest:
                largest = size
                lrg_id = prop['tokenid']
                name = prop['name']
                artist = prop['createdBy']

    print(f"Largest File Size: {largest / (1<<20):,.2f} MB, Token ID: {lrg_id} - "\
          f"{name} by {artist}")

def smallest_file(data):
    """
    Finds the token with the smallest filesize on SuperRare.

    Args:
        data: JSON metadata.
    """
    #Initial placeholders for comparison
    size = 5000000
    smallest = 5000000
    sml_id = None

    for prop in data:
        if 'media' in prop:
            size = int(prop['media']['size'])
            if size < smallest and prop['tokenid'] is not None and size != 0:
                smallest = size
                sml_id = prop['tokenid']
                name = prop['name']
                artist = prop['createdBy']

    print(f"Smallest File Size: {smallest} Bytes, Token ID: {sml_id} - {name} by {artist}")

def total_fs(data):
    """
    Calculate the total and average filesize of all media on SuperRare.

    Args:
        data: JSON metadata.
    """
    total_size = 0
    for prop in data:
        if 'media' in prop:
            size = int(prop['media']['size'])
            total_size += size

    print(f"Total Media Filesize: {total_size/ (1<<30):,.2f} GB")
    print(f"Overall Average Filesize: {(total_size / len(data) / (1<<20)):,.2f} MB")

def common_attribute(data, media: bool, attribute):
    """
    Take an attribute in SR metadata, and return the 10 most common values of that attribute

    Args:
        data: JSON metadata.
        media: True/False value for when the attribute is in the 'media' object.
        attribute: Name of JSON property to search in the metadata.
    """

    #The following for loop has some separate handling for attributes in the 'media' object,
    #and for the 'tags' property, as these are structured differently in the metadata.
    #Ultimately, every non-empty value should be added to cmn_list no matter which
    #attribute is provided.

    cmn_list = []

    for prop in data:
        att = None
        if media:
            if 'media' in prop and attribute in prop['media']:
                att = prop['media'][attribute]
        elif attribute == 'tags':
            if 'tags' in prop:
                att = prop['tags']
        else:
            if attribute in prop:
                att = prop[attribute]
        if att is not None:
            if attribute == 'tags':
                for tag in att:
                    cmn_list.append(tag)
            else:
                cmn_list.append(att)

    #Get the 10 most common values in the list.
    counted_att = Counter(cmn_list).most_common(10)

    print(f"Most common {attribute}:")
    for count in counted_att:
        print(f"{count[0]}: {count[1]}")

def linebreak():
    """
    Separates function outputs in terminal.
    """
    print("-" * 40)

def main():
    """
    Main function, call other functions here.
    """

    data = load_json()

    print("Data for Token ID Range: 8584 - 39581")
    linebreak()

    mimetype_info(data)
    linebreak()

    size_info(data)
    linebreak()

    large_size_trend(data)
    linebreak()

    largest_file(data)
    linebreak()

    smallest_file(data)
    linebreak()

    common_attribute(data, True, "dimensions")
    linebreak()

    common_attribute(data, False, "tags")
    linebreak()

    common_attribute(data, False, "name")
    linebreak()

    common_attribute(data, False, "createdBy")
    linebreak()

    common_attribute(data, False, "yearCreated")
    linebreak()

    total_fs(data)
    linebreak()

if __name__ == '__main__':
    main()
