from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError
)

# create a password hasher.
ph = PasswordHasher(
    time_cost=2,
    memory_cost=19456,
    parallelism=1
)

def hash_password(password):
    # argon2id creates a unique random salt.
    return ph.hash(password)

def verify_password(stored_hash, password):
    try:
        return ph.verify(stored_hash, password)

    except (VerifyMismatchError, VerificationError):
        return False