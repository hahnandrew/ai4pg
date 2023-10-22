import hashlib
def hash_string(string):
    string_bytes = string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string_bytes)
    hashed_string = sha256_hash.hexdigest()
    return hashed_string
