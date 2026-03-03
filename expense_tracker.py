import os, json, argparse
from datetime import datetime
FILE_NAME = "expenses.json"

#  -- Data Management --

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        
def save_expenses(expenses):
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)
        
def add_expense(description, amount):
    if amount<=0:
        print("Error: Amount must be greater than zero.")
        return
    expenses = load_expenses()
    new_id = expenses[-1]['id'] + 1 if expenses else 1
    
    new_expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount
    }
    
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")
    
def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    
    print(f"{'ID': <5} {'Date':<12}{'Description':<20}{'Amount':<10}")
    print("-" * 50)
    for exp in expenses:
        print(f"{exp['id']:<5} {exp['date']: <12} {exp['description']:<20} ${exp['amount']:<10}")
    
def delete_expense(expense_id):
    expenses = load_expenses()
    updated = [e for e in expenses if e['id'] != expense_id]
    
    if len(expenses) == len(updated):
        print(f"Error: Expense with ID {expense_id} not found.")
    else:
        save_expenses(updated)
        print("Expense deleted successfully")
        
def show_summary(month=None):
    expenses = load_expenses()
    current_year = datetime.now().year
    
    if month:
        filtered = [
            e['amount'] for e in expenses
            if datetime.strptime(e['date'], "%Y-%m-%d").month == month
            and datetime.strptime(e['date'], "%Y-%m-%d").year == current_year
        ]
        month_name = datetime(current_year, month, 1).strftime("%B")
        print(f"Total expenses for {month_name}: ${sum(filtered)}")
    else:
        total = sum(e['amount'] for e in expenses)
        print(f"Total expenses: ${total}")
        
def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True, help="Description of the expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount of the expense")
    
    subparsers.add_parser("list")
    
    del_parser = subparsers.add_parser("delete")
    del_parser.add_argument("--id", type=int, required=True, help="ID of expense to delete")
    
    sum_parser = subparsers.add_parser("summary")
    sum_parser.add_argument("--month", type=int, help="Month number (1-12) to summarize")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "list":
        list_expenses()
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "summary":
        show_summary(args.month)
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()