<h1>🧠 SmartCache – Python In-Memory Caching System</h1>
SmartCache is a flexible and intelligent in-memory cache system implemented in Python. It supports:

Multiple eviction policies (LRU, LFU, FIFO)

Time-to-Live (TTL) based expiration

Thread-safe operations for concurrent reads/writes

Multi-type value support (strings, lists, numbers, etc.)

Scalable batch writes, efficient eviction of old/stale data

✅ Key Features
🔁 Eviction Policies: FIFO, LRU, LFU

🕒 TTL Expiry: Auto-removal of expired items using time checks

🔒 Thread-safe using RLock for concurrency

🧠 Custom Search Support via predicate function

⚡ Batch Write for multiple key-value pairs

🔎 Efficient Reads & Deletes

🛠️ How It Works<br><br>
✅ Example: cache.write("a", "apple")
This line calls the write() method, which:

Checks for existing/expired keys.

Evicts a key if capacity is full (based on eviction policy).

Stores the key-value pair in an internal OrderedDict:
<br>
self.cache["a"] = "apple"<br>
Tracks TTL using a dictionary:

<br>
self.expiry["a"] = current_time + ttl (if given)<br>
Internally, your cache now contains: {"a": "apple"}

<h1>🔑 Core Methods</h1>
<h3>1. write(key, value, ttl=None)</h3>
Stores a key-value pair in cache.

Supports batch insert using a list of tuples.

Automatically evicts a key if the cache is full.

Sets TTL if provided.<br>

<h3>2. read(key)</h3>
Returns the value for a key if it exists and is not expired.

Updates LRU/LFU frequency.<br>

<h3>3. delete(key)</h3>
Removes a key from cache, TTL tracker, frequency, and LRU list.<br>

<h3>4. search(predicate)</h3>
Custom search using lambda functions or any function that takes (key, value) and returns a Boolean.<br><br>

<h1>🔁 Eviction Policies</h1>
📦 FIFO (First-In, First-Out)
Evicts the oldest inserted key when full.<br>

📌 LRU (Least Recently Used)
Evicts the least recently accessed key.<br>

📉 LFU (Least Frequently Used)
Evicts the least frequently accessed key.<br>

Frequency updated on every read.

<h1>⏳ TTL Expiry Handling</h1>
TTL (Time-To-Live) allows you to set expiry duration in seconds. Expired keys are automatically removed when:

A read/write is attempted.
Internal _remove_expired_keys() checks each TTL.

<u>Example:</u>
cache.write("a", "apple", ttl=2)<br>
time.sleep(3)<br>
print(cache.read("a"))  # Outputs: None (expired)<br><br>
<h1>🧵 Thread-Safety & Concurrent Access</h1>
Uses threading.RLock() for safe access in multi-threaded environments.

Every method (read, write, delete, etc.) uses a with self.lock: block to prevent race conditions.

<h1>⚙️ Handling Large Datasets & Memory Limits</h1>
capacity defines the maximum number of items allowed.

When full, the cache evicts old entries based on the eviction policy.

Supports scalable batch writes like:

cache.write([("a", "apple"), ("b", "banana")], ttl=5)
💡 Supports Multiple Data Types
You can store:
<br>
Strings: "apple"
<br>
Numbers: 123
<br>
Lists: ["a", "b", "c"]
<br>
Even complex objects (like dictionaries)
<br>
This is possible because Python dictionaries allow any hashable key and any value.

🔍 Custom Search Example

<h2># Find all keys whose value is a fruit name<br></h2>
results = cache.search(lambda k, v: isinstance(v, str) and v in ["apple", "banana"])<br>
📦 Test Case Highlights<br>
✅ Test Case 1: LRU with TTL
<br>
cache = SmartCache(capacity=2, eviction_policy='LRU')<br>
cache.write("a", 5, ttl=2)<br>
cache.write("b", 6, ttl=2)<br>
cache.write("c", "cherry", ttl=2)  # Evicts "a"<br>
time.sleep(5)<br>
print(cache.read("a"))  # Expired, returns None<br><br>
✅ Test Case 2: LFU + Batch Writes
<br>
cache = SmartCache(capacity=10, eviction_policy='LFU')<br>
cache.write([("a", "apple"), ("b", "tomato")], ttl=2)<br>
for _ in range(3): cache.read("b")  # b has high frequency<br>
cache.write("e", "mango", ttl=2)    # Evicts least used key<br><br>
✅ Test Case 3: FIFO with List Values
<br>
cache = SmartCache(capacity=2, eviction_policy='FIFO')<br>
cache.write("a", ["hello", "hye"], ttl=5)<br>
cache.write("b", "banana", ttl=5)<br>
cache.write("c", "cherry", ttl=5)  # Evicts "a"
