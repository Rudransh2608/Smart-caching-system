#test_cache for searching algorithm for int and str data types.

from cache import SmartCache
cache = SmartCache(capacity=2, eviction_policy='FIFO')
cache.write("x", 12345, ttl=5)
cache.write("y", "banana", ttl=5)

result = cache.search(lambda k, v: isinstance(v, (int, str)) and '1' in str(v))
result2 = cache.search(lambda k, v: isinstance(v, str) and 'a' in v)
print("Search result:", result2)
print("Search result:", result)