import requests

myURL = "http://www.pcrhero.org:8000/submit"
params = {"user":"joshmd@bu.edu", "app": "Cello", "circuit":"lacZ", "score":1}
r = requests.post(myURL, params=params)
print(r.text)


params = {"user":"joshmd@bu.edu", "app": "Double Dutch", "circuit":"lacA", "score":1}
s = requests.post(myURL, params=params)
print(s.text)