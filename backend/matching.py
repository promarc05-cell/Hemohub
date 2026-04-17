import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def find_nearby_donors(request_lat, request_lng, donors, radius_km, blood_group):
    """
    Filter donors based on distance and blood group compatibility.
    """
    matches = []
    for donor in donors:
        if donor.blood_group == blood_group and donor.is_available:
            dist = haversine(request_lat, request_lng, donor.latitude, donor.longitude)
            if dist <= radius_km:
                matches.append({
                    "donor_id": donor.donor_id,
                    "distance": round(dist, 2),
                    "reliability": donor.reliability_score
                })
    
    # Sort by reliability and then distance
    matches.sort(key=lambda x: (-x['reliability'], x['distance']))
    return matches
