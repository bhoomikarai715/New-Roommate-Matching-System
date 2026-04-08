def calculate_compatibility(user, candidate):
    """
    Weighted scoring algorithm for matching.
    Sleep Pattern: 20%
    Personality: 15%
    Cleanliness: 18%
    Noise Tolerance: 18%
    Room Preference: 15%
    Profession: 7%
    Social Energy Rating: 7%
    Total: 100%
    """
    score = 0.0
    
    # 1. Sleep Pattern (20)
    if user.sleep_pattern == candidate.sleep_pattern:
        score += 20
    elif user.sleep_pattern == "Flexible" or candidate.sleep_pattern == "Flexible":
        score += 10
    else:
        score += 5
        
    # 2. Personality (15)
    if user.personality == candidate.personality:
        score += 15
    elif "Ambivert" in [user.personality, candidate.personality]:
        score += 7.5
    else:
        score += 3.75
        
    # 3. Cleanliness (18)
    cleanliness_levels = ["Messy but Tidy", "Moderate", "Organized", "Very Clean"]
    try:
        u_idx = cleanliness_levels.index(user.cleanliness)
        c_idx = cleanliness_levels.index(candidate.cleanliness)
        diff = abs(u_idx - c_idx)
        if diff == 0:
            score += 18
        elif diff == 1:
            score += 10.8 # 60% of 18
        else:
            score += 3.6 # 20% of 18
    except ValueError:
        if user.cleanliness == candidate.cleanliness:
            score += 18
        else:
            score += 3.6
            
    # 4. Noise Tolerance (18)
    noise_levels = ["Very Quiet", "Quiet", "Moderate", "Lively", "Party Friendly"]
    try:
        u_idx = noise_levels.index(user.noise_tolerance)
        c_idx = noise_levels.index(candidate.noise_tolerance)
        diff = abs(u_idx - c_idx)
        if diff == 0:
            score += 18
        elif diff == 1:
            score += 10.8 # 60%
        else:
            score += 3.6 # 20%
    except ValueError:
        if user.noise_tolerance == candidate.noise_tolerance:
            score += 18
        else:
            score += 3.6
            
    # 5. Room Preference (15)
    if user.room_preference == candidate.room_preference:
        score += 15
        
    # 6. Profession (7)
    if user.profession == candidate.profession:
        score += 7
    else:
        score += 2.1 # 30% of 7
        
    # 7. Social Energy (7)
    u_se = user.social_energy_rating or 5
    c_se = candidate.social_energy_rating or 5
    se_diff = abs(u_se - c_se)
    # Score = 1 - (diff / 9) scaled to 7
    score += (1 - (se_diff / 9.0)) * 7
    
    # Scale and clamp (50-100)
    final_score = max(50.0, min(100.0, score))
    return round(final_score, 2)
