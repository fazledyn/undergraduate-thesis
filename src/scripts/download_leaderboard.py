import requests as r
import json

url = "https://api.crowdtangle.com/leaderboard?token=MJ9s6vpH51U5K4LK6183EC3Nd9BG8jGxrA1axFlT&count=10&listId=1748775"

out = r.get(url=url)

print(out.text)

with open("./leaderboard.json", "w", encoding="utf-8") as outfile:
    outfile.write(out.text)