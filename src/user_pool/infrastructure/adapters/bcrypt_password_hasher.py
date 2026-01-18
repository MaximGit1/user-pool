from bcrypt import gensalt, hashpw

from user_pool.domain.value_objects.raw_password import RawPassword


class BcryptPasswordHasher:
    def hash(self, raw_password: RawPassword) -> bytes:
        return hashpw(raw_password.value.encode(), gensalt())
