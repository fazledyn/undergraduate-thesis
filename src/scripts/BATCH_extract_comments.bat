@echo off

set data_dir=%1

for %%i in ("%data_dir%\*") do (
  python extract_from_json.py "%%i"
)