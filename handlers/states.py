from aiogram.fsm.state import State, StatesGroup


class AddExpenseState(StatesGroup):
    choosing_category = State()
    entering_amount = State()
    entering_description = State()


class AddIncomeState(StatesGroup):
    entering_amount = State()
    entering_description = State()
