import time
import random
import math
import sys
import os

# Configure path to import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Driver
from geoalchemy2.elements import WKTElement

def simulate():
    db = SessionLocal()
    print("Geo-Guard simulation started...")
    print("Sending real-time GPS coordinates...")

    # Load or create 15 drivers for the demo
    drivers = db.query(Driver).limit(15).all()
    if not drivers:
        print("Creating new drivers for simulation...")
        for i in range(15):
            new_d = Driver(name=f"Driver-{i+1}")
            db.add(new_d)
        db.commit()
        drivers = db.query(Driver).all()

    # Center coordinates for Nairobi
    nairobi_lat, nairobi_lon = -1.286389, 36.817223
    
    # Angle for each driver so they start in different directions
    angles = [random.uniform(0, 2 * math.pi) for _ in range(len(drivers))]
    distances = [random.uniform(0, 0.05) for _ in range(len(drivers))] 

    try:
        while True:
            for i, driver in enumerate(drivers):
                # Move the driver
                # 0.001 approx = 110 meters
                speed = random.uniform(0.0005, 0.002)
                
                # Some drivers (e.g., index 0 and 5) will move far away to exit the zone
                if i in [0, 5]:
                    speed = 0.005

                distances[i] += speed
                
                # Calculate new position
                new_lat = nairobi_lat + (distances[i] * math.sin(angles[i]))
                new_lon = nairobi_lon + (distances[i] * math.cos(angles[i]))

                # Update in PostGIS
                driver.last_position = WKTElement(f'POINT({new_lon} {new_lat})', srid=4326)
            
            db.commit()
            print(f"Update: {len(drivers)} positions updated.", end='\r')
            time.sleep(2)  # Simulate a ping every 2 seconds

    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        db.close()

if __name__ == "__main__":
    simulate()