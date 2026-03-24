import urllib.request
import urllib.error
import json
import ssl
import sys

url = "https://reserva-kuiz.onrender.com/api/users/register/"
data = {"first_name": "Test", "email": "test-new@test.com", "password1": "password123", "password2": "password123"}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
req.add_header('Content-Type', 'application/json')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    print("Testing POST to", url)
    response = urllib.request.urlopen(req, context=ctx, timeout=120)
    print("Status:", response.status)
    print(response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print(e.read().decode())
except Exception as e:
    print("Other Error:", e)

