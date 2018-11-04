#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys

from search_net import SearchNet

def get_api_key():
    API_KEY_FILE = os.path.join(sys.path[0], "youtubeApiKey.txt")
    with open(API_KEY_FILE, "r") as f:
        return f.read().strip()

API_KEY = get_api_key()

def main():
    sn = SearchNet(API_KEY)
    sn.get_results("house m.d")

if __name__ == "__main__":
    main()
