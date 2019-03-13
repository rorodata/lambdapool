import pytest
from lambdapool.utils import convert_size

testdata_convert_size = [
    [0, '0 B'],
    [1024, '1.0 KB']
]

@pytest.mark.parametrize('bytes,sizestring', testdata_convert_size)
def test_convert_size(bytes, sizestring):
    assert convert_size(bytes) == sizestring
