from datetime import datetime as dt
import pytest
from lambdapool.utils import convert_size, datestr, run_command

testdata_convert_size = [
    [0, '0 B'],
    [1024, '1.0 KB']
]

@pytest.mark.parametrize('bytes,sizestring', testdata_convert_size)
def test_convert_size(bytes, sizestring):
    assert convert_size(bytes) == sizestring

testdata_datestr = [
    [dt(2019, 1, 10, 12, 0, 0), dt(2019, 1, 10, 12, 0, 0), 'Just now'],
    [dt(2019, 1, 10, 11, 59, 50), dt(2019, 1, 10, 12, 0, 0), '10 seconds ago'],
    [dt(2019, 1, 10, 11, 40, 0), dt(2019, 1, 10, 12, 0, 0), '20 minutes ago'],
    [dt(2019, 1, 10, 10, 0, 0), dt(2019, 1, 10, 12, 0, 0), '2 hours ago'],
    [dt(2019, 1, 9, 12, 0, 0), dt(2019, 1, 10, 12, 0, 0), '1 day ago'],
    [dt(2019, 1, 8, 12, 0, 0), dt(2019, 1, 10, 12, 0, 0), '2 days ago'],
    [dt(2019, 1, 6, 12, 0, 0), dt(2019, 1, 10, 12, 0, 0), 'January  6'],
    [dt(2018, 12, 10, 12, 0, 0), dt(2019, 1, 10, 12, 0, 0), 'December 10, 2018'],
    [dt(2019, 1, 11, 12, 0, 0), dt(2019, 1, 10, 12, 0, 0), '1 day from now'],
    [dt(2019, 1, 12, 12, 0, 0), dt(2019, 1, 10, 12, 0, 0), '2 days from now'],
]

@pytest.mark.parametrize('then,now,datestring', testdata_datestr)
def test_datestr(then, now, datestring):
    assert datestr(then, now) == datestring

def test_run_command():
    assert run_command('ls').returncode == 0
