from datetime import datetime


class User:
    def __init__(
        self,
        email: str,
        username: str,
        id: int | None = None,
        is_active: bool = True,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.email = email
        self.username = username
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self._validate()

    def _validate(self):
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email")
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def __repr__(self):
        return f"<User {self.username}>"
