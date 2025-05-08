import pytest

from src.tests.search_logic import map_positions


def test_map_positions_order_and_duplicates():
    # given talent_ids with duplicates and a mapping of distances
    talent_ids = ['x', 'y', 'x']
    distances = {'x': 0.05, 'y': 0.15}
    # sample positions rows
    position_rows = [
        {'talent_id': 'x', 'pos': 'dev'},
        {'talent_id': 'x', 'pos': 'lead'},
        {'talent_id': 'y', 'pos': 'merc'}
    ]

    output = map_positions(talent_ids, position_rows, distances)
    assert len(output) == 3
    assert output[0]['talent_id'] == 'x' and output[0]['positions'][0]['pos'] == 'dev'
    assert output[1]['talent_id'] == 'y' and output[1]['positions'][0]['pos'] == 'merc'
    assert output[2]['talent_id'] == 'x' and output[2]['positions'][1]['pos'] == 'lead'
