from bitmapindex import BitmapIndex


def test_init_with_run_length_encoding():
    b = BitmapIndex("0.1.70.1.")
    run_length_values = [False, True, False, False, False, False, False, False, False, True]
    for i in range(10):
        assert b[i] == run_length_values[i]


def test_generate_run_length_encoding():
    b = BitmapIndex()
    run_length_values = [False, True, False, False, False, False, False, False, False, True]
    for i in range(10):
        b[i] = run_length_values[i]
    assert "0.1.70.1." == b.rle


def test_setting_values_around_the_bucket_boundary():
    b = BitmapIndex()
    for i in range(b.bucket_size-5, b.bucket_size+5):
        b[i] = True
    assert len(b._data.keys()) == 2
    assert b.rle == "{0}0.101.".format(b.bucket_size-5)


def test_ints_property():
    b = BitmapIndex()
    ints = [1, 5, 7, 8, 10]
    for i in ints:
        b[i] = True

    b_ints = b.ints
    assert frozenset(b_ints) == frozenset(ints)
    assert len(b_ints) == len(ints)


def test_get_set_item():
    b = BitmapIndex()

    # int key should return bool
    assert isinstance(b[0], bool)
    assert b[0] == False

    # non-int key should raise TypeError
    try:
        b["foo"]
    except TypeError:
        assert True
    else:
        assert False

    # check that setting an item to true returns a true value
    b[0] = True
    assert b[0] == True

    # non-int key should raise TypeError
    try:
        b["foo"] = True
    except TypeError:
        assert True
    else:
        assert False


def test_delitem():
    b = BitmapIndex()

    # non-int key should raise TypeError
    try:
        del b["foo"]
    except TypeError:
        assert True
    else:
        assert False

    del b[0]


def test_contains():
    b = BitmapIndex()

    # non-int key should raise TypeError
    try:
        "foo" in b
    except TypeError:
        assert True
    else:
        assert False

    assert (5 in b) == False


def test_len():
    b = BitmapIndex()

    assert len(b) == 0

    ints = [1, 5, 7, 8, 10]
    for i, v in enumerate(ints, 1):
        b[v] = True
        assert len(b) == i


def test_mofify():
    b = BitmapIndex()

    try:
        b._modify("foo", True)
    except TypeError:
        assert True
    else:
        assert False

    try:
        b._modify(0, "foo")
    except TypeError:
        assert True
    else:
        assert False

    try:
        b._modify(0, True)
    except TypeError:
        assert False
    else:
        assert True


def test_enable_disable():
    b = BitmapIndex()

    b.enable(0)
    assert b[0] == True

    b.disable(0)
    assert b[0] == False

