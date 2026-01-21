import requests, json
r = requests.get('http://127.0.0.1:8188/history/f6075d87-272f-4d28-8f30-f25c4bdfdb4c')
h = r.json()
msgs = h.get('f6075d87-272f-4d28-8f30-f25c4bdfdb4c', {}).get('status', {}).get('messages', [])
err = [m for m in msgs if m[0] == 'execution_error']
if err:
    print("Error Type:", err[0][1].get('exception_type'))
    print("Error Message:", err[0][1].get('exception_message'))
    print("Traceback:")
    for line in err[0][1].get('traceback', [])[:5]:
        print(line[:200])
else:
    print("No error found")
