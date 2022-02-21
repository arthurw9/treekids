import os.path
import secrets
import json

CONFIG_FILE = 'config.json'

def CreateIfNotExists():
  if os.path.exists(CONFIG_FILE):
    return
  with open(CONFIG_FILE, 'w') as f:
    c = {}
    c['SECRET_KEY'] = secrets.token_hex()
    f.write(json.dumps(c, sort_keys=True, indent=2))

def GetConfig():
  CreateIfNotExists()
  with open(CONFIG_FILE, 'r') as f:
    s = f.read()
  return json.loads(s)

    
