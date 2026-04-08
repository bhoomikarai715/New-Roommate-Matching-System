import urllib.request
import json

req = urllib.request.Request(
    'https://new-roommate-matching-system.vercel.app/api/auth/firebase', 
    data=b'{}', 
    headers={'Content-Type': 'application/json'}
)

try:
    urllib.request.urlopen(req)
except Exception as e:
    print(e.read().decode())
