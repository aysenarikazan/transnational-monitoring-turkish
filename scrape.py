#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import csv
import time
from tqdm import tqdm
import sys

test_url = "http://181.csb.gov.tr"

def load_keywords():
    keywords = list()
    filepath = "keywords.txt"
    count = 0
    with open(filepath) as fp:
        lines = fp.readlines()
        for line in lines:
            count += 1
            line_text = line.strip()
            keywords.append(line_text)
    return keywords

def read_links_from_file(filename):
    filepath = filename
    links = list()
    count = 0
    with open(filepath) as fp:
        lines = fp.readlines()
        for line in lines:
            count += 1
            line_text = line.strip()
            if line_text.startswith("http") and (not line_text.endswith(".pdf") and not line.endswith(".rar")):
                links.append(line_text)
    return links

def get_source_code(url):
    html_text = requests.get(url, timeout=2).text
    return html_text

def search_keyword(source, keyword):
    source = source.lower()
    keyword = keyword.lower()

    if keyword in source:
        return 1
    else:
        return 0
    # occurence = source.count(keyword)
    # return occurence

def extract_text_from_source(source):
    bs = BeautifulSoup(source, "html.parser")
    text = bs.get_text()
    cleaned_text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    return cleaned_text

def write_csv_file(filename, occ_dict):
    env_csv = open(filename + ".csv", "w")
    with env_csv:
        writer = csv.writer(env_csv)
        for k, v in occ_dict.items():
            writer.writerow([k, v])

def main(file_name):
    file_name = file_name.replace(".txt", "")
    keywords = load_keywords()
    link_list = read_links_from_file(file_name + ".txt")

    score_dict = dict()
    
    for link in tqdm(link_list, desc="Links"):
        # print("LINK: " + link)
        try:
            source = get_source_code(link)
            source = extract_text_from_source(source)
            for keyword in keywords:
                # print("KEYWORD: " + link)
                occ = search_keyword(source, keyword)
                if keyword in score_dict:
                    score_dict[keyword] += occ
                else:
                    score_dict[keyword] = occ
                # print("Link: " + link + " Keyword: " + keyword + " Occurence: " + str(occ))
        except KeyboardInterrupt:
            print("Ctrl+C pressed...")
            print("Current progress saved to: " + file_name + ".csv")
            write_csv_file(file_name, score_dict)
            sys.exit(1)
        except:
            pass
            # print("Skipped link: " + link)

    print("Values saved to: " + file_name + ".csv")
    write_csv_file(file_name, score_dict)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./scrape.py filename.txt")
    else:
        main(sys.argv[1])
    
