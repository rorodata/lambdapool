import pytest

from lambdapool import LambdaPool
from lambdapool.exceptions import LambdaPoolError

from .fixtures import TestFunctionBase

@pytest.mark.skip(reason='The tests are errroing out due to some AWS quirks. Needs to be revisited')
@pytest.mark.aws
class TestPool(TestFunctionBase):
    def test_map_no_error(self, function_fib):
        pool = LambdaPool(2, "test-function")
        result = pool.map("algorithms.fib", range(2))
        assert result == [0, 1]

    def test_map_timeout(self, function_fib):
        pool = LambdaPool(2, "test-function")
        with pytest.raises(LambdaPoolError):
            pool.map("algorithms.fib", range(50))

    def test_map_function_error(self, function_fib):
        pool = LambdaPool(2, "test-function")
        with pytest.raises(LambdaPoolError):
            pool.map("algorithms.fib", range(51))

    def test_apply_no_error(self, function_fib):
        pool = LambdaPool(2, "test-function")
        result = pool.apply("algorithms.fib", args=(2,))
        assert result == 1

    def test_apply_timeout(self, function_fib):
        pool = LambdaPool(2, "test-function")
        with pytest.raises(LambdaPoolError):
            pool.apply("algorithms.fib", range(50))

    def test_apply_function_error(self, function_fib):
        pool = LambdaPool(2, "test-function")
        with pytest.raises(LambdaPoolError):
            pool.apply("algorithms.fib", range(51))

    def test_apply_async_no_error(self, function_fib):
        pool = LambdaPool(2, "test-function")
        result = pool.apply_async("algorithms.fib", args=(2,))

        while not result.ready():
            assert result.get() == 1

    def test_apply_async_timeout(self, function_fib):
        pool = LambdaPool(2, "test-function")
        with pytest.raises(LambdaPoolError):
            result = pool.apply_async("algorithms.fib", range(50))

            while not result.ready():
                result.get()

    def test_apply_async_function_error(self, function_fib):
        pool = LambdaPool(2, "test-function")
        with pytest.raises(LambdaPoolError):
            result = pool.apply_async("algorithms.fib", range(51))

            while not result.ready():
                result.get()

