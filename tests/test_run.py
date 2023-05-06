import unittest
import logging
from qgate_perf.parallel_executor import ParallelExecutor
from qgate_perf.parallel_probe import ParallelProbe
from qgate_perf.run_setup import RunSetup
from qgate_perf.executor_helper import ExecutorHelper
from qgate_perf.run_return import RunReturn
import time


#def prf_GIL_impact(return_key, return_dict, run_setup: RunSetup):
def prf_GIL_impact(run_return: RunReturn, run_setup: RunSetup):
    """ Function for performance testing"""
    try:
        # init (contain executor synchonization, if needed)
        probe = ParallelProbe(run_setup)

        while (True):

            # START - performance measure for specific part of code
            probe.start()

            for r in range(run_setup.bulk_row * run_setup.bulk_col):
                time.sleep(0)

            # STOP - performance measure specific part of code
            if probe.stop():
                break

        # return outputs
        run_return.probe=probe

    except Exception as ex:
        # return outputs in case of error
        run_return.probe=ParallelProbe(None, ex)

class TestCaseRun(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_one_shot(self):
        generator = ParallelExecutor(prf_GIL_impact,
                                     label="GIL_impact",
                                     detail_output=True,
                                     output_file="../output/test_gil_impact_test.txt")

        generator.one_shot()

    def test_run(self):
        generator = ParallelExecutor(prf_GIL_impact,
                                     label="GIL_impact",
                                     detail_output=True,
                                     output_file="../output/test_gil_impact_test.txt")

        setup=RunSetup(duration_second=5, start_delay=0)
        generator.run(2, 2, setup)

    def test_run_executor(self):
        generator = ParallelExecutor(prf_GIL_impact,
                                     label="GIL_impact",
                                     detail_output=True,
                                     output_file="../output/test_gil_impact_test.txt")

        setup=RunSetup(duration_second=1, start_delay=0)
        generator.run_executor([[1,1], [1,2], [2,2]], setup)

    def test_run_bulk_executor(self):
        generator = ParallelExecutor(prf_GIL_impact,
                                     label="GIL_impact",
                                     detail_output=True,
                                     output_file="../output/test_gil_impact_test.txt")

        setup=RunSetup(duration_second=1, start_delay=0)
        generator.run_bulk_executor(bulk_list=[[1,1], [1,10], [1,100]],
                                    executor_list=[[1,1], [1,2], [2,2]],
                                    run_setup=setup)

    def test_run_stress_test(self):
        generator = ParallelExecutor(prf_GIL_impact,
                                     label="GIL_impact",
                                     detail_output=True,
                                     output_file=None)

        setup=RunSetup(duration_second=30, start_delay=0)
        generator.run(4, 8, setup)


if __name__ == '__main__':
    unittest.main()