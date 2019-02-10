import redis
from redis import Redis
from PIL import Image
from io import BytesIO
from redis.sentinel import Sentinel

# List of allowed connections
sentinel_list = [
  ('127.0.0.1', 5000),
  ('10.0.0.45', 8001),
  ('10.0.0.45', 8001)
]

# Use BytesIO not StringIO, see: https://stackoverflow.com/a/32075279/6435921
output = BytesIO()
# Open image and save it
im = Image.open("test_image.jpg")
im.save(output, format=im.format)
# Upload it to redis
r = redis.StrictRedis(host='localhost')
r.set('imagedata', output.getvalue())
output.close()
print(r.get('imagedata'))


r = redis.Redis(host="localhost", port=6379, db=0)

