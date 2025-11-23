from datetime import datetime, timedelta
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
            pass 

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
    """Adds a visitor if they are not a duplicate and the wait time is respected."""
    ensure_file()
    last_data = get_last_visitor()
    current_time = datetime.now()
    
    if last_data:
        last_name, last_time_str = last_data
        
        # Rule 1: Duplicate Check
        if last_name == visitor_name:
            raise DuplicateVisitorError(f"{visitor_name} was the last visitor.")
        
        # Rule 2: 5-Minute Wait Check
        try:
            last_time = datetime.fromisoformat(last_time_str)
        except ValueError:
            # If timestamp is malformed, we allow entry to avoid blocking indefinitely
            pass 
        else:
            time_diff = current_time - last_time
            if time_diff < timedelta(minutes=5):
                raise EarlyEntryError("Must wait 5 minutes between visitors.")
            
    # Append to file
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {current_time.isoformat()}\n")

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