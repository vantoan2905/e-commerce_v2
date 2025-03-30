from sqlalchemy.orm import Session
from src.database.models.user_product.user_session import UserSession
from datetime import datetime, timedelta

class SessionService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: int, session_id: str):
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            session_start=datetime.utcnow(),
            session_end=datetime.utcnow() + timedelta(hours=24) 
        )
        self.db.add(session)
        self.db.commit()

    def validate_session(self, session_id: str):
        session = self.db.query(UserSession).filter(UserSession.session_id == session_id).first()
        if session and session.session_end > datetime.utcnow():
            return session.user_id
        return None
