import pandas as pd
import sys


def main():

    input_file = sys.argv[1]
    comment_csv_path = sys.argv[2]

    df_main = pd.read_csv(input_file)
    
    df_main["comment_neg"] = 0
    df_main["comment_pos"] = 0
    df_main["comment_total"] = 0

    for i, row in df_main.iterrows():

        csv_file = row["comment_csv"]
        df_comment = pd.read_csv(f"{comment_csv_path}/{csv_file}.csv")

        n_pos = len(df_comment[ df_comment["label"] == "positive" ])
        n_neg = len(df_comment[ df_comment["label"] == "negative" ])

        df_main.at[i, "comment_pos"] = n_pos
        df_main.at[i, "comment_neg"] = n_neg 
        df_main.at[i, "comment_total"] = n_pos + n_neg

        print(f"Row {i+1} done!")

    print("Saving New CSV...")
    df_main.to_csv(f"{comment_csv_path}{input_file}", index=False)

    pass


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print()
        print("*********************** help **************************")
        print("$ python count_comments.py <INPUT_CSV> <COMMENT_CSV_PATH>")
        print("Example: $ python count_comments.py ../rafsan.csv ../rafsan/pred/")
        print()
        exit(-1)

    main()