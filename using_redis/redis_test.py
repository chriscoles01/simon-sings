import redis
from redis import Redis
from redis.sentinel import Sentinel

# List of allowed connections
sentinel_list = [
  ('127.0.0.1', 5000),
  ('10.0.0.45', 8001),
  ('10.0.0.45', 8001)
]

r = Redis('127.0.0.1', socket_timeout=0.1, db=0)

# set key “foo” with value “bar”
print(r.set('foo', 'bar'))

# set the value for key “foo”
print(r.get('foo'))


r = redis.Redis(host="localhost", port=6379, db=0)

r.set('foo', 'bar')

