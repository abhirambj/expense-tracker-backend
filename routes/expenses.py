from fastapi import APIRouter, HTTPException
from models.expenses import Expense

router = APIRouter()

expenses = []


@router.post("/expenses/")
def create_expense(expense: Expense):
    if expenses:
        expense.id = expenses[-1].id + 1
    else:
        expense.id = 1

    expense_data = expense.model_dump()
    expense_data["id"] = expense.id
    expenses.append(expense_data)
    return {"message": "Expense created successfully", "data": expense_data}


@router.get("/expenses/")
def get_expenses():
    return {"expenses": expenses}


@router.put("/expenses/{expense_id}")
def update_expense(expense_id: int, update_expense: Expense):
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            update_expense_data = update_expense.model_dump()
            update_expense_data["id"] = expense_id
            expenses[index] = update_expense_data
            return {"message": "Expense updated successfully", "data": update_expense_data}
    raise HTTPException(status_code=404, detail="Expense not found")


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            del expenses[index]
            return {"message": "Expense deleted successfully"}
    raise HTTPException(status_code=404, detail="Expense not found")
