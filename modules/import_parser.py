import json
import csv

def _check_rows(labels, rows):
  for row in rows:
    for label in labels:
      val = row[label]
      if val is None: return
      try:
        row[label] = float(val)
      except: return
  return rows

def parse_json(labels, data):
  res = json.load(data)
  return _check_rows(labels, res)

def parse_csv(labels, data):
  res = csv.DictReader(data, skipinitialspace=True)
  return _check_rows(labels, list(res))

UPLOAD_TYPES = {
    # 'text/xml': xml,
    'application/json': parse_json,
    'text/csv': parse_csv,
}

def get_parser(filetype):
  return UPLOAD_TYPES[filetype]
