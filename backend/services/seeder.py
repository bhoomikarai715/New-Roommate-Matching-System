import csv
import random
import os
from sqlalchemy.orm import Session
from backend.models.entities import RoommateRecord

def seed_database(db: Session, csv_path: str = None):
    if csv_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(base_dir, "backend", "data", "Girls_pg_hostel_CSV_data-1.csv")
        
    if db.query(RoommateRecord).first() is not None:
        # Already seeded
        return
    
    if not os.path.exists(csv_path):
        print(f"CSV not found at {csv_path}. Skipping seed.")
        return

    # Mapping dictionaries
    sleep_pattern_map = {"Night": "Night Owl (12-2 AM)", "Morning": "Morning (7-9 AM)", "Evening": "Evening (10-11 PM)"}
    profession_map = {"Developer": "Software Developer", "Supporting Staff": "Other", "Customer Support": "Other"}
    cleanliness_map = {"Organised": "Organized", "Both": "Moderate", "Messy": "Messy but Tidy"}
    noise_tol_map = {"Noisy": "Lively", "Quiet": "Quiet"}
    room_prefs = ["single-bedded", "studio", "shared"]

    records_to_insert = []
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            work_shift = row.get("work_shift", "")
            profession = row.get("profession", "")
            cleanliness = row.get("cleanliness", "")
            noise_pref = row.get("noise_preference", "")
            social_energy = row.get("social_energy_rating", "")
            
            try:
                energy_val = int(social_energy)
            except (ValueError, TypeError):
                energy_val = 5

            record = RoommateRecord(
                full_name=row.get("user_name", ""),
                sleep_pattern=sleep_pattern_map.get(work_shift, str(work_shift)),
                profession=profession_map.get(profession, str(profession)),
                personality=str(row.get("personality", "")),
                cleanliness=cleanliness_map.get(cleanliness, str(cleanliness)),
                noise_tolerance=noise_tol_map.get(noise_pref, str(noise_pref)),
                bedtime=str(row.get("bedtime", "")),
                wake_time=str(row.get("wake_time", "")),
                sleep_type=str(row.get("sleep_type", "")),
                social_energy_rating=energy_val,
                room_preference=random.choice(room_prefs)
            )
            records_to_insert.append(record)

    db.add_all(records_to_insert)
    db.commit()
    print(f"Database seeded with {len(records_to_insert)} records.")
