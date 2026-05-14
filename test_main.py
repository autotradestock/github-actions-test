from main import add, greet

def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

def test_greet():
    result = greet("테스트")
    assert result == "안녕하세요, 테스트!"
