
import bcrypt
import sys

def verify_laravel_hash(password, hashed):
    print(f"Original hashed: {hashed}")
    # Laravel uses $2y$, bcrypt uses $2b$
    if hashed.startswith('$2y$'):
        hashed = '$2b$' + hashed[4:]
    print(f"Modified hashed: {hashed}")
    
    pwd_bytes = password.encode('utf-8')
    hash_bytes = hashed.encode('utf-8')
    
    try:
        result = bcrypt.checkpw(pwd_bytes, hash_bytes)
        print(f"Bcrypt result: {result}")
        return result
    except Exception as e:
        print(f"Bcrypt error: {e}")
        return False

# The hash we found in DB for chirantan@joinroster.co
test_hash = '$2y$10$rUd/0Tig9Ub5cHJyigqJGO1jt8vOxPTONK9tJQ8.5ceZrCM2r97kW'
test_password = 'Test@1234'

verify_laravel_hash(test_password, test_hash)
