from typing import List, Dict, Any

def map_positions(
    talent_ids: List[str],
    position_rows: List[Dict[str, Any]],
    id_to_distance: Dict[str, float]
) -> List[Dict[str, Any]]:

    results = []
    for tid in talent_ids:
        positions = [row for row in position_rows if row['talent_id'] == tid]
        results.append({
            'talent_id': tid,
            'distance': id_to_distance.get(tid),
            'positions': positions
        })

    return results