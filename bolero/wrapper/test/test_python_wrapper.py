import os
import numpy as np
from bolero.wrapper import CppBLLoader
from nose.tools import assert_true, assert_false, assert_equal


CURRENT_PATH = os.sep.join(__file__.split(os.sep)[:-1])
LIBRARY_CONFIG_FILE = CURRENT_PATH + os.sep + "test_library_config.txt"
if not CURRENT_PATH:
    LIBRARY_CONFIG_FILE = "test_library_config.txt"


def test_load_optimizer():
    bll = CppBLLoader()
    bll.load_config_file(LIBRARY_CONFIG_FILE)
    opt = bll.acquire_optimizer("pso_optimizer")
    n_params = 5
    params = np.zeros(n_params)
    opt.init(n_params)
    opt.get_next_parameters(params)
    opt.set_evaluation_feedback(np.zeros(1))


def test_load_environment():
    bll = CppBLLoader()
    bll.load_config_file(LIBRARY_CONFIG_FILE)
    env = bll.acquire_environment("mountain_car")
    env.init()
    n_inputs = env.get_num_inputs()
    n_outputs = env.get_num_outputs()
    inputs = np.zeros(n_inputs)
    outputs = np.zeros(n_outputs)
    env.reset()
    env.get_outputs(outputs)
    env.set_inputs(inputs)
    env.step_action()
    assert_false(env.is_evaluation_done())
    feedbacks = np.ones(1)
    assert_equal(1, env.get_feedback(feedbacks))
    assert_true(np.all(feedbacks == 0))
    assert_false(env.is_behavior_learning_done())


def tst_load_behavior_search():
    os.environ["BL_CONF_PATH"] = CURRENT_PATH
    bll = CppBLLoader()
    bll.load_config_file(LIBRARY_CONFIG_FILE)
    bhs = bll.acquire_behavior_search("Python")
    n_inputs = 1
    n_outputs = 1
    bhs.init(n_inputs, n_outputs)
    beh = bhs.get_next_behavior()
    outputs = np.zeros(n_outputs)
    beh.get_outputs(outputs)
    inputs = np.zeros(n_inputs)
    beh.set_inputs(inputs)
    bhs.set_evaluation_feedback(np.zeros(1))