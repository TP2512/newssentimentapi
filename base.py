import base64

lp = ["mongodb://mongodb-service:27017", "news_aggregator_db",
      "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", "HS256", "60", "/code"]
for i in lp:
    encoded = base64.b64encode(i.encode()).decode()
    print(encoded)
