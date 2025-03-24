from sqlalchemy.orm import Session
from src.database.models.user import User
from src.schemas.user_schema import UserCreate
import hashlib



class UserService:
    def __init__(self, db: Session):
        """
        Initialize the UserService class with a database connection.

        Parameters:
            db: A database connection object used to interact with the database.
        """
        self.db = db
    def get_user_by_username(self, user_name: str):
        """
        Retrieve a specific user by username.

        Parameters:
            user_name (str): The username.

        Returns:
            User: The user record, or None if not found.
        """
        return self.db.query(User).filter(User.username == user_name).first()

    def create_user(self, username: str, email: str, password: str, name: str, phone_number: str, role: str, created_at: str):
        """
        Create a new user in the database.

        Parameters:
            username (str): The username.
            email (str): The email address.
            password (str): The password.
            name (str): The user's name.
            phone_number (str): The phone number.
            role (str): The user's role.
            created_at (str): The timestamp when the user was created.

        Returns:
            User: The newly created user record.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db_user = User(username=username, email=email, password=hashed_password, name=name, phone_number=phone_number, role=role, created_at=created_at)
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    def get_user_by_email(self, email: str):
        """
        Retrieve a specific user by email.

        Parameters:
            email (str): The email address.

        Returns:
            User: The user record, or None if not found.
        """
        
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all_users(self):
        """
        Retrieve all users from the database.

        Returns:
            list[User]: A list of all user records in the database.
        """

        return self.db.query(User).all()
    def update_user(self, username: str, email: str, password: str, name: str, phone_number: str, role: str, created_at: str):
        """
        Update an existing user in the database.

        Parameters:
            username (str): The username.
            email (str): The email address.
            password (str): The password.
            name (str): The user's name.
            phone_number (str): The phone number.
            role (str): The user's role.
            created_at (str): The timestamp when the user was created.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return False

        user.email = email
        user.password = hashlib.sha256(password.encode()).hexdigest()
        user.name = name
        user.phone_number = phone_number
        user.role = role
        user.created_at = created_at
        self.db.commit()
        return True
    
    def delete_user(self, username: str):
        """
        Delete an existing user from the database.

        Parameters:
            username (str): The username.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True


