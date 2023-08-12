from tdd_2_attempt import Bottle

def test_verse():
    bottle = Bottle()
    expected = f"""99 bottles of beer on the wall, 99 bottles of beer.
Take one down and pass it around, 98 bottles of beer on the wall."""
    assert bottle.verse(1) == expected

def test_last_but_2_verse():
    bottle = Bottle()
    expected = f"""2 bottles of beer on the wall, 2 bottles of beer.
Take one down and pass it around, 1 bottle of beer on the wall."""
    assert bottle.verse(98) == expected
    
def test_last_but_1_verse():
    bottle = Bottle()
    expected = f"""1 bottle of beer on the wall, 1 bottle of beer.
Take one down and pass it around, no more bottles of beer on the wall."""
    assert bottle.verse(99) == expected

def test_last_verse():
    bottle = Bottle()
    expected = f"""No more bottles of beer on the wall, no more bottles of beer.
Go to the store and buy some more, 99 bottles of beer on the wall."""
    assert bottle.verse(100) == expected

def test_last_4_verses():
    bottle = Bottle()
    expected = f"""3 bottles of beer on the wall, 3 bottles of beer.
Take one down and pass it around, 2 bottles of beer on the wall.

2 bottles of beer on the wall, 2 bottles of beer.
Take one down and pass it around, 1 bottle of beer on the wall.

1 bottle of beer on the wall, 1 bottle of beer.
Take one down and pass it around, no more bottles of beer on the wall.

No more bottles of beer on the wall, no more bottles of beer.
Go to the store and buy some more, 99 bottles of beer on the wall."""
    assert bottle.verses(97, 100) == expected

def test_last_but_3_verse():
    bottle = Bottle()
    expected = f"""3 bottles of beer on the wall, 3 bottles of beer.
Take one down and pass it around, 2 bottles of beer on the wall."""
    assert bottle.verses(97,97) == expected
    