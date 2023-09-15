from googletrans import Translator
import avro

import pandas as pd
import sys
import re


#   Translator
trans = Translator()


def filter_bangla(a):
    out = "".join(i for i in a if i in [".","।"] or 2432 <= ord(i) <= 2559 or ord(i)== 32)
    re.sub(' +', ' ', out)
    return out


def translate_to_bangla(x):
    try:
        x = trans.translate(x, dest='bn').text
    except:
        pass
    return x

def main():
    input_file = sys.argv[1]
    print("Input File:", input_file)

    df = pd.read_json(input_file)
    df = df["commentText"]

    #   If you want to drop first row
    #   Author post their own comments
    df = df.iloc[1:]

    #   Data Filtering
    df = df.apply(lambda x: x.replace('\n', ' ').replace('\t', ' '))
    df = df.apply(lambda x: x.replace('"', "'").replace('\"', '\''))
    df = df.apply(lambda x: x.replace(',', ""))

    #   Translation
    df = df.apply(lambda x: translate_to_bangla(x))
    df = df.apply(lambda x: avro.parse(x))

    #   Renaming Input File
    temp = input_file.split(" ")
    input_file = "".join(temp)
    temp = input_file.split("(")
    input_file = "".join(temp)
    temp = input_file.split(")")
    input_file = "".join(temp)
    input_file = input_file.replace(".json", "")

    with open(f"{input_file}.csv", "w", encoding="utf-8") as out_file:
        out_file.write("sentence1\n")
        for sentence in df:
            out_file.write(f"\"{avro.parse(sentence, in_ascii=False)}\"\n")

    print("Conversion Complete!")


if __name__ == "__main__":
    main()