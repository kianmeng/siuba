import pandas as pd
import numpy as np
import pytest

from siuba.dply.verbs import case_when
from pandas.testing import assert_series_equal
from numpy.testing import assert_equal
from siuba.siu import _

DATA = pd.DataFrame({
    'x': [0,1,2],
    'y': [10, 11, 12]
    })


@pytest.fixture
def data():
    return DATA.copy()


@pytest.mark.parametrize("k,v, res", [
    (True, 1,     [1]*3),
    (True, False, [False]*3),
    (True, _.y,   [10, 11, 12]),
    (True, lambda _: _.y, [10, 11, 12]),
    (_.x < 2, 0,  [0, 0, None]),
    (_.x < 2, "small", ["small", "small", None]),
    (_.x < 2, _.y, [10, 11, None]),
    (lambda _: _.x < 2, 0,  [0, 0, None]),
    #(np.array([True, True, False]), 0, [0, 0, None])
    ])
def test_case_when_single_cond(k, v, res, data):
    out = case_when(data, {k: v})

    assert_series_equal(out, pd.Series(res))


def test_case_when_cond_order(data):
    out = case_when(data, {
        lambda _: _.x < 2  :  0,
        True               : 999
        })

    assert_series_equal(out, pd.Series([0, 0, 999]))

