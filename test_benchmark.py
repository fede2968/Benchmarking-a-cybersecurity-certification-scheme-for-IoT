import pytest
import explore_PERFORMACE
import dataset_generator

def setup_data(config):
    system = dataset_generator.main([config])
    for s in system:
        old_score = s["score"]
        actual_score = s["score_new"]
        new_system = s["micro_new"]
        old_system = s["grouped_properties"]
        N = 1
        J = 1
        t = explore_PERFORMACE.explore(old_score, actual_score, new_system, old_system, N, J)
        return new_system, t

def generate_test_data(config):
    system = dataset_generator.main([config])
    for s in system:
        old_score = s["score"]
        actual_score = s["score_new"]
        new_system = s["micro_new"]
        old_system = s["grouped_properties"]
        return old_score, actual_score, new_system, old_system

@pytest.mark.parametrize("config", dataset_generator.setting)
@pytest.mark.benchmark(group="execute", min_rounds=1000, max_time=10.0, disable_gc = True, warmup = True)
def test_execute_benchmark(config, benchmark):
    new_system, t = setup_data(config)
    benchmark(explore_PERFORMACE.execute, new_system, t)


@pytest.mark.parametrize("config", dataset_generator.setting)
@pytest.mark.benchmark(group="explore", min_rounds=1000, max_time=10.0, disable_gc = True, warmup = True)
def test_explore(config, benchmark):
    old_score, actual_score, new_system, old_system = generate_test_data(config)
    benchmark(explore_PERFORMACE.explore, old_score, actual_score, new_system, old_system, N=1, J=1)



