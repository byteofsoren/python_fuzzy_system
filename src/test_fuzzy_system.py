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
        "temp,price",[
            (0,1),
            (5,1),
            (10,1),
            (-10,1),
            (20,-10),
        ]
)
def test_rule_creation(temp,price):
    cold = fuzzy.fuzzy_member_pointlist([[5,1],[10,0]])
    warm = fuzzy.fuzzy_member_pointlist([[5,0],[10,1]])
    cheap = fuzzy.fuzzy_member_pointlist([[10,1],[15,0]])
    expensive = fuzzy.fuzzy_member_pointlist([[10,0],[15,1]])
    r1 = cold*cheap
    r1b = cheap*cold
    r2 = cold + cheap
    r2b = cheap + cold
    r3 = cold + warm*expensive
    r3b = warm*expensive + cold
    r5 = warm*r2
    r5b = r2*warm
    cold.fire(temp)
    warm.fire(temp)
    cheap.fire(price)
    expensive.fire(price)
    assert r1() == r1b()
    assert r2() == r2b()
    assert r3() == r3b()
    assert r5() == r5b()
    # assert np.round(r1(), 2)  == tc
    # assert np.round(r2(), 2)  == tw


