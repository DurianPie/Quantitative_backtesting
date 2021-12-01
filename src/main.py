from pickle import TRUE
from src.backtest.back_test_log import *
from src.Strategy import *
from src.IOUtils import *
from src.backtest.config import *
from src.backtest.eval_strategy import *
from src.log import *
import random
import os
import pandas as pd
from src.backtest.back_test import *

if __name__ == '__main__':
    data = IOUtils('../data/data.pkl')
    # data = {}

    back_test = BackTest()

    config = BaseConfig()
    back_test.set_config(config)

    back_test.test(data)

    eval_result = back_test.eval()

    if eval_result:
        print("after %d test, %s is good strategy!" % (int(config.n_sample), config.strategy))
    else:
        print("after %d test, %s is bad strategy!" % (int(config.n_sample), config.strategy))

    back_test.save_eval_result()
    back_test.save_log()
