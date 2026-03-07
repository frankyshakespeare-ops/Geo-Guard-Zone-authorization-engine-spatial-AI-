import sys
import os

# Added the root path so that Python can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
# IMPORTANT: We import all the models so that Base knows them
from app.models import Zone, Driver, Order 

def reset_database():
    print(" Connexion à la base de données...")
    
    # 1. Delete everything to start from scratch
    print("  Deleting all tables (drop_all)...")
    Base.metadata.drop_all(bind=engine)
    
    # 2. Recreate the tables
    print("  Creating new tables (create_all)...")
    Base.metadata.create_all(bind=engine)
    
    print("  Database initialized successfully!")

if __name__ == "__main__":
    try:
        reset_database()
    except Exception as e:
        print(f" Error during update : {e}")