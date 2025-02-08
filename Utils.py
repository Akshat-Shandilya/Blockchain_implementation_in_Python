# Utils.py
 
from hashlib import sha256 

def hash256(*args):
    t = ""
    h = sha256()
    for arg in args:
        t += str(arg)
    h.update(t.encode('utf-8'))
    return h.hexdigest()