from database.models import SessionLocal, User


def get_or_create_user(telegram_id: int, username: str = None) -> User:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
            session.commit()
            session.refresh(user)
        return user
    finally:
        session.close()


def get_user(telegram_id: int) -> User | None:
    session = SessionLocal()
    try:
        return session.query(User).filter(User.telegram_id == telegram_id).first()
    finally:
        session.close()


def set_language(telegram_id: int, language: str):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.language = language
            session.commit()
    finally:
        session.close()


def get_language(telegram_id: int) -> str:
    user = get_user(telegram_id)
    return user.language if user else "en"
