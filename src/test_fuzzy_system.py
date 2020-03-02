import pytest
import fuzzy_system as fuzzy
import numpy as np


@pytest.mark.parametrize(
        "fire, c,w,h",[
            (0,1,0,0),
            (10,0,1,0),
            (20,0,0,1),
            (5,0.5,1,0),
            (15,0,1,0.5),
            ]

)
def test_input( fire,c,w,h):
    cold = fuzzy.fuzzy_member_pointlist([[0,1],[10,0]])
    warm = fuzzy.fuzzy_member_pointlist([[0,0],[5,1],[15,1],[20,0]])
    hot  = fuzzy.fuzzy_member_pointlist([[10,0],[20,1]])
    assert np.round(cold.fire(fire),2) ==  c
    assert np.round(warm.fire(fire),2) ==  w
    assert np.round(hot.fire(fire),2)  == h

def test_novalue():
    with pytest.raises(Exception) as e_info:
        cold = fuzzy.fuzzy_member_pointlist()



@pytest.mark.parametrize(
        "fire,fuzzy_and,fuzzy_or",[
            (0,0,1),
            (10,0,1),
            (20,0,0),
        ]
)
def test_and(fire,fuzzy_and, fuzzy_or):
    cold = fuzzy.fuzzy_member_pointlist([[0,1],[10,0]])
    warm = fuzzy.fuzzy_member_pointlist([[0,0],[5,1],[15,1],[20,0]])
    r1 = cold*warm
    r2 = cold + warm
    assert np.round(r1(fire),1) == np.round(fuzzy_and,1)
    assert np.round(r2(fire),1) == np.round(fuzzy_or,1)

