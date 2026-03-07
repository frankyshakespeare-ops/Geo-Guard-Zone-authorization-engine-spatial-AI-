import sys
import os
import random
from app.database import SessionLocal
from app.models import Order
from geoalchemy2.elements import WKTElement

# We add the parent folder to Python's search path so that it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
# ... the rest of your imports

db = SessionLocal()

def create_cluster(base_lat, base_lon, count, spread=0.005):
    """Generates a group of orders around a central point"""
    for _ in range(count):
        lat = base_lat + random.uniform(-spread, spread)
        lon = base_lon + random.uniform(-spread, spread)
        point = f"POINT({lon} {lat})"
        order = Order(
            lat=lat, 
            lon=lon, 
            position=WKTElement(point, srid=4326)
        )
        db.add(order)

# 1. Dense cluster in the CBD (15 orders)
create_cluster(-1.283, 36.823, 15)

# 2. Cluster in Westlands (10 orders)
create_cluster(-1.265, 36.808, 10)

# 3. Isolated points (Noise for DBSCAN)
create_cluster(-1.310, 36.750, 3, spread=0.02)

try:
    db.commit()
    print(" 28 test orders inserted successfully!")
except Exception as e:
    db.rollback()
    print(f" Error : {e}")
finally:
    db.close()