from encrypted_id import encode, decode


def test_encode():
    assert decode(encode(10)) == 10
    # e = encode(20)
    # print(e)
    # assert decode(u'IGqVjhm4x7ntEUuyA-sFTg..') == 20
