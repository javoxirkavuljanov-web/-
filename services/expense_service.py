from datetime import datetime
from database.models import SessionLocal, Expense, User


def add_expense(telegram_id: int, amount: float, category: str, description: str = None) -> Expense:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        expense = Expense(
            user_id=user.id,
            amount=amount,
            category=category,
            description=description,
            date=datetime.utcnow(),
        )
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense
    finally:
        session.close()


def delete_expense(expense_id: int, telegram_id: int) -> bool:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        expense = session.query(Expense).filter(
            Expense.id == expense_id, Expense.user_id == user.id
        ).first()
        if expense:
            session.delete(expense)
            session.commit()
            return True
        return False
    finally:
        session.close()


def get_expenses(telegram_id: int, limit: int = None) -> list[Expense]:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        query = session.query(Expense).filter(Expense.user_id == user.id).order_by(Expense.date.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    finally:
        session.close()


def get_expenses_by_month(telegram_id: int, year: int, month: int) -> list[Expense]:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        return (
            session.query(Expense)
            .filter(
                Expense.user_id == user.id,
                Expense.date >= datetime(year, month, 1),
                Expense.date < datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1),
            )
            .order_by(Expense.date.desc())
            .all()
        )
    finally:
        session.close()


def get_total_expenses(telegram_id: int) -> float:
    expenses = get_expenses(telegram_id)
    return sum(e.amount for e in expenses)
