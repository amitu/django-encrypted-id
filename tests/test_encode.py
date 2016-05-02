from encrypted_id import encode, decode


def test_encode():
    assert decode(encode(10)) == 10
