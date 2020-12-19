import pytest
import json
import navie_solver

actual_metadata: dict
expected_metadata: dict


@pytest.fixture(autouse=True, scope='module')
def run_code():
    navie_solver.main()
    global actual_metadata
    global expected_metadata
    with open('actual_metadata.json', 'r') as f:
        actual_metadata = json.load(f)
    with open('expected_metadata.json', 'r') as f:
        expected_metadata = json.load(f)


def test_scene_2():
    metadata = actual_metadata['scene_2.json']
    assert metadata['succeed']
    assert metadata['total_time'] < 1
    assert metadata['number_of_steps'] <= 5
    assert metadata['number_of_moves'] <= 7
    assert metadata['remained_distance'] == 0


def test_scene_5():
    metadata = actual_metadata['scene_5.json']
    assert metadata['succeed']
    assert metadata['total_time'] < 1
    assert metadata['number_of_steps'] <= 7
    assert metadata['number_of_moves'] <= 21
    assert metadata['remained_distance'] == 0


def test_all_inputs():
    for scene in expected_metadata:
        actual = actual_metadata[scene]
        expected = expected_metadata[scene]
        if expected['succeed']:
            assert actual['succeed'], f'scene {scene} failed'
            assert actual['number_of_moves'] <= expected['number_of_moves'], \
                f'scene {scene} number of moves is longer than expected'
            assert actual['number_of_steps'] <= expected['number_of_steps'], \
                f'scene {scene} number of steps is longer than expected'
        assert actual['total_time'] < expected['total_time'] + 1, f'scene {scene} time is longer than expected'
        assert actual['remained_distance'] <= expected['remained_distance'], \
            f'scene {scene} remained distance is longer than expected'
