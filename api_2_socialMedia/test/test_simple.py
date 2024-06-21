### Here if you are testing something file name should contain test like test_king or test_ping or ping_test
### condition is true for function too


def test_add():
    a, b = 1, 2
    assert a + b == 3

def test_two():
    data = {"a":1, "b":2}
    expected = {"a":1}

    assert expected.items()<= data.items()
