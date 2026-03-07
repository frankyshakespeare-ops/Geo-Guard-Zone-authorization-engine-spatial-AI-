import random
import sys
import os
import requests
from app.database import SessionLocal
from app.models import Driver
from geoalchemy2 import WKTElement

# Path configuration to find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Definition of zones in Nairobi 
min_lon, max_lon = 36.7, 36.9
min_lat, max_lat = -1.35, -1.20

db = SessionLocal()

try:
    # 2. Massive insertion of drivers in Nairobi
    total_sages = 100 
    drivers = []
    print(f" Phase 1: Insertion of {total_sages} drivers in Nairobi ")
    
    for i in range(total_sages):
        lon = random.uniform(min_lon, max_lon)
        lat = random.uniform(min_lat, max_lat)
        geom = WKTElement(f"POINT({lon} {lat})", srid=4326)
        drivers.append(Driver(last_position=geom)) 

    db.bulk_save_objects(drivers)
    db.commit()
    print(f" {total_sages} drivers insérés avec succès.")

    # 3. Insertion of drivers outside of Nairobi 
    rebelles = [
        {"id": 88888, "lat": -0.717, "lon": 36.435, "name": "Naivasha Rebel"},
        {"id": 99999, "lat": -4.043, "lon": 39.668, "name": "Mombasa Rebel"},
    ]

    print("Phase 2: Test of anomalies via the API")
    for r in rebelles:
        payload = {
            "driver_id": r["id"],
            "lat": r["lat"],
            "lon": r["lon"],
            "weather": "sunny"
        }
        try:
            # Make a POST request to the API to check if the driver can accept an order
            response = requests.post("http://127.0.0.1:8000/can_accept_order", json=payload)
            if response.status_code == 200:
                status = response.json().get("authorized")
                print(f"Driver {r['id']} ({r['name']}) -> Autorisé: {status} (Attendu: False)")
            else:
                print(f" Erreur API pour {r['name']}: {response.status_code}")
        except Exception as e:
            print(f" Erreur de connexion : Ton serveur Uvicorn est-il lancé ?")

finally:
    db.close()