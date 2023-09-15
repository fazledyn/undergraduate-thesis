from datetime import datetime, timedelta

import pandas as pd
import sys


def main():

    csv_file = sys.argv[1]
    df = pd.read_csv(csv_file)

    df["timestamp"] = None
    df["week_day"] = None
    df["time_slot"] = 0

    for i, row in df.iterrows():
        date = row["Post Created Date"]
        time = row["Post Created Time"]

        dt_string = f"{date}::{time}"
        date_time = datetime.strptime(dt_string, "%d-%m-%y::%H:%M:%S")

        #   Even though Crowdtangle says that their exported time is in UTC
        #   it appears that it's actually UTC+1 - Crosschecked with Facebook
        timestamp = date_time + timedelta(hours=5)
        weekday = timestamp.strftime("%A").lower()
        time_slot = timestamp.hour + 1

        df.at[i, "week_day"] = weekday
        df.at[i, "time_slot"] = time_slot
        df.at[i, "timestamp"] = timestamp

    df.to_csv(f"{csv_file}_out.csv", index=False)
    print("Features extracted!")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("*******************************")
        print("$ python extract_features.py <CSV_NAME>")
        print()    
        exit(-1)

    main()
