import pandas as pd
import random
import os
from sqlalchemy.orm import Session
from backend.models.entities import RoommateRecord

def seed_database(db: Session, csv_path: str = "backend/data/Girls_pg_hostel_CSV_data-1.csv"):
    if db.query(RoommateRecord).first() is not None:
        # Already seeded
        return
    
    if not os.path.exists(csv_path):
        print(f"CSV not found at {csv_path}. Skipping seed.")
        return

    df = pd.read_csv(csv_path)

    # Mapping dictionaries
    sleep_pattern_map = {"Night": "Night Owl (12-2 AM)", "Morning": "Morning (7-9 AM)", "Evening": "Evening (10-11 PM)"}
    profession_map = {"Developer": "Software Developer", "Supporting Staff": "Other", "Customer Support": "Other"}
    cleanliness_map = {"Organised": "Organized", "Both": "Moderate", "Messy": "Messy but Tidy"}
    noise_tol_map = {"Noisy": "Lively", "Quiet": "Quiet"}
    room_prefs = ["single-bedded", "studio", "shared"]

    records_to_insert = []
    
    for _, row in df.iterrows():
        mapped_sp = sleep_pattern_map.get(row.get("work_shift", ""), str(row.get("work_shift", "")))
        mapped_prof = profession_map.get(row.get("profession", ""), str(row.get("profession", "")))
        mapped_cln = cleanliness_map.get(row.get("cleanliness", ""), str(row.get("cleanliness", "")))
        mapped_noise = noise_tol_map.get(row.get("noise_preference", ""), str(row.get("noise_preference", "")))
        
        record = RoommateRecord(
            full_name=row.get("user_name"),
            sleep_pattern=mapped_sp,
            profession=mapped_prof,
            personality=str(row.get("personality", "")),
            cleanliness=mapped_cln,
            noise_tolerance=mapped_noise,
            bedtime=str(row.get("bedtime", "")),
            wake_time=str(row.get("wake_time", "")),
            sleep_type=str(row.get("sleep_type", "")),
            social_energy_rating=int(row.get("social_energy_rating", 5) if pd.notna(row.get("social_energy_rating")) else 5),
            room_preference=random.choice(room_prefs)
        )
        records_to_insert.append(record)

    db.add_all(records_to_insert)
    db.commit()
    print(f"Database seeded with {len(records_to_insert)} records.")
