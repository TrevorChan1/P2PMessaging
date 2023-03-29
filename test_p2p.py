import session_init

def test_nameExists():
    assert session_init.p2pMessager("Trevdawg", 0) == -1