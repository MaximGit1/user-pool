from datetime import UTC, datetime
from logging import getLogger

from user_pool.domain.entities import User
from user_pool.domain.ports import PasswordHasher, UserIDGenerator
from user_pool.domain.value_objects import Email, RawPassword, Username

log = getLogger(__name__)


class UserService:
    """User flow service"""

    def __init__(
        self,
        id_generator: UserIDGenerator,
        password_hasher: PasswordHasher,
    ) -> None:
        self._id_generator = id_generator
        self._password_hasher = password_hasher

    def create_user(
        self, username: str, email: str, raw_password: str
    ) -> User:
        """Creates a new user with validation"""
        return User(
            _id=self._id_generator.generate(),
            _username=Username.safe(username),
            _email=Email.safe(email),
            _hashed_password=self._password_hasher.hash(
                RawPassword.safe(raw_password)
            ),
            _created_at=datetime.now(UTC),
        )
