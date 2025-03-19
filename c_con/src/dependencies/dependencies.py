import os
from dotenv import load_dotenv
from typing import Optional

class Config:
    """
    Loads environment variables for database configuration.
    """

    def __init__(self) -> None:
        """
        Initialize the Config class and load required environment variables.
        
        Raises:
            ValueError: If any required environment variable is missing.
        """
        load_dotenv()
        self._db_name: Optional[str] = os.getenv("DB_NAME")
        self._db_user: Optional[str] = os.getenv("DB_USER")
        self._db_password: Optional[str] = os.getenv("DB_PASSWORD")
        self._db_host: Optional[str] = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        self._db_port: Optional[int] = int(db_port) if db_port is not None else None

        # Ensure all required environment variables are present
        if None in (self._db_name, self._db_user, self._db_password, self._db_host, self._db_port):
            missing = [
                var_name for var_name, value in {
                    "DB_NAME": self._db_name,
                    "DB_USER": self._db_user,
                    "DB_PASSWORD": self._db_password,
                    "DB_HOST": self._db_host,
                    "DB_PORT": self._db_port,
                }.items() if value is None
            ]
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    def get_user(self) -> str:
        """
        Get the database user.

        Returns:
            str: The database user.
        """
        return self._db_user  # type: ignore

    def get_password(self) -> str:
        """
        Get the database password.

        Returns:
            str: The database password.
        """
        return self._db_password  # type: ignore

    def get_host(self) -> str:
        """
        Get the database host.

        Returns:
            str: The database host.
        """
        return self._db_host  # type: ignore

    def get_port(self) -> int:
        """
        Get the database port.

        Returns:
            int: The database port.
        """
        return self._db_port  # type: ignore

    def get_name(self) -> str:
        """
        Get the database name.

        Returns:
            str: The database name.
        """
        return self._db_name  # type: ignore
