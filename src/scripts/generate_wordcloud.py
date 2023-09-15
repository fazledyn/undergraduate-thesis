from matplotlib import pyplot as plt
from wordcloud import WordCloud
from bnlp.corpus import stopwords, punctuations
from collections import Counter

import numpy as np
import pandas as pd
import json
import sys
import re


def clean(text):
    text = re.sub('[%s]' % re.escape(punctuations), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('\xa0', '', text)
    return text


file_name = sys.argv[1]
df = pd.read_csv(file_name)
msg = df["Message"]

print("File name:", file_name)
print("Total Message:", msg.shape)

word_list = []
for each in msg:
    if type(each) == type("string"):
        words = each.split()
        word_list.extend(words)

word_list_filtered = []
word_cloud_text = ""
regex = r"[\u0980-\u09FF]+"


for each in word_list:
    if len(each) > 3:
        if "http" not in each:
            if "\\" not in each:
                if "/" not in each:
                    if "@" not in each:
                        if ":" not in each:
                            if "," not in each:
                                if "(" not in each:
                                    if ")" not in each:
                                        if "!" not in each:
                                            if "'" not in each:
                                                if "?" not in each:
                                                    if "’" not in each:
                                                        if "." not in each:
                                                            if "-" not in each:
                                                                if "\"" not in each:
                                                                    # each = clean(each)
                                                                    # no need to clean for bangla
                                                                    if each.isascii():
                                                                        word_list_filtered.append(each.lower())
                                                                        word_cloud_text += " " + each.lower()

print("Word List:", len(word_list))
print("Word List (Filtered):", len(word_list_filtered))

#   Wordcloud UI
font = "./fonts/siliguri.ttf"
word_cloud = WordCloud(font_path=font, collocations=False, background_color="white", width=3 * 1024, height= 3 * 512).generate(word_cloud_text)

#   Wordcloud Figure
plt.figure( figsize=(40,20) )
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout()
plt.savefig(f"{file_name}_wordcloud.png")

#   Counting Words in List and Sorting
word_count = Counter(word_list_filtered)
word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

#   Dump is JSON with Formatting
with open(f"{file_name}_wcount.json", "w") as file:
    file.write(json.dumps(word_count, indent="\t"))
