from datetime import datetime
from database.models import SessionLocal, Income, User


def add_income(telegram_id: int, amount: float, description: str = None) -> Income:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        income = Income(
            user_id=user.id,
            amount=amount,
            description=description,
            date=datetime.utcnow(),
        )
        session.add(income)
        session.commit()
        session.refresh(income)
        return income
    finally:
        session.close()


def delete_income(income_id: int, telegram_id: int) -> bool:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        income = session.query(Income).filter(
            Income.id == income_id, Income.user_id == user.id
        ).first()
        if income:
            session.delete(income)
            session.commit()
            return True
        return False
    finally:
        session.close()


def get_incomes(telegram_id: int, limit: int = None) -> list[Income]:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        query = session.query(Income).filter(Income.user_id == user.id).order_by(Income.date.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    finally:
        session.close()


def get_incomes_by_month(telegram_id: int, year: int, month: int) -> list[Income]:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        return (
            session.query(Income)
            .filter(
                Income.user_id == user.id,
                Income.date >= datetime(year, month, 1),
                Income.date < datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1),
            )
            .order_by(Income.date.desc())
            .all()
        )
    finally:
        session.close()


def get_total_income(telegram_id: int) -> float:
    incomes = get_incomes(telegram_id)
    return sum(i.amount for i in incomes)
