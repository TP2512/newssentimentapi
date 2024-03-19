import base64

lp = ["mongodb://mongodb:27017",]
for i in lp:
    encoded_username = base64.b64encode(i.encode()).decode()
    print(encoded_username)
