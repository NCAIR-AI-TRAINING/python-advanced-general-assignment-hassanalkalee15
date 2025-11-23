from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    """Creates visitors.txt if it does not exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass # Create empty file

def get_last_visitor():
    """Returns the (name, timestamp) of the last visitor, or None."""
    if not os.path.exists(FILENAME):
        return None
    
    with open(FILENAME, "r") as f:
        lines = f.readlines()
        
    if not lines:
        return None
        
    # Parse the last line: "Name | ISO_TIMESTAMP"
    last_line = lines[-1].strip()
    try:
        name, timestamp = last_line.split(" | ")
        return name, timestamp
    except ValueError:
        return None

def add_visitor(visitor_name):
    """Adds a visitor if they are not a duplicate."""
    ensure_file()
    last_data = get_last_visitor()
    
    # Check for Duplicate Visitor
    if last_data:
        last_name, _ = last_data
        if last_name == visitor_name:
            raise DuplicateVisitorError(f"{visitor_name} was the last visitor.")
            
    # Add new visitor
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {datetime.now().isoformat()}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
