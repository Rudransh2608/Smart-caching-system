from cache import SmartCache
import time

""" test_cache for LFU eviction strategy with multiple key value pairs in the form of a list showing storage management, scalibilty and 
operations like read , write ,delete.
"""
cache = SmartCache(capacity=10, eviction_policy='LFU')

cache.write([("a", "apple"), ("b", "tomato"), ("c", "cherry")],ttl=2)
cache.write("d", "GUAVA", ttl=2)


for _ in range(3):
    cache.read("b")

print("After 2 writes and b accessed 3 times:", list(cache.cache.keys()))

cache.write("e", "mango", ttl=2)  

print("After 3rd write (LFU eviction expected):", list(cache.cache.keys()))

print("Read b:", cache.read("b"))
print("Read a:", cache.read("a"))  
print("Read e:", cache.read("e")) 