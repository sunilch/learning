Udacity Logo
sunil chidara
Catalog
Nanodegree
Design of Computer Programs

DASHBOARD

CLASSROOM

MATERIALS

DISCUSSION

OVERVIEW
View Edit History
cs212 »

Unit 3 Code
Contents

1 Unit 3 Code
1.1 regex_interpreter.py
1.2 regex_compiler.py
1.3 regex_generator.py
1.4 decorators.py
1.5 grammar.py
regex_interpreter.py

def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text) or 1):
        m = match(pattern, text[i:])
        if m is not None: return m

def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = matchset(pattern, text)
    if remainders:
        shortest = min(remainders, key = len)
        return text[:len(text)-len(shortest)]

def matchset(pattern, text):
    "Match pattern at start of text; return a set of remainders of text."
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y, text)
    elif 'dot' == op:
        return set([text[1:]]) if text else null
    elif 'oneof' == op:
        return set([text[1:]]) if text.startswith(tuple(x)) else null
    elif 'eol' == op:
        return set(['']) if text == '' else null
    elif 'star' == op:
        return (set([text]) |
                set(t2 for t1 in matchset(x, text)
                    for t2 in matchset(pattern, t1) if t1 != text))
    else:
        raise ValueError('unknown pattern: %s' % pattern)

null = frozenset()

def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y

def lit(string):  return ('lit', string)
def seq(x, y):    return ('seq', x, y)
def alt(x, y):    return ('alt', x, y)
def star(x):      return ('star', x)
def plus(x):      return ('seq', x, ('star', x))
def opt(x):       return alt(lit(''), x) #opt(x) means that x is optional
def oneof(chars): return ('oneof', tuple(chars))
dot = ('dot', )
eol = ('eol', )

def test():
    assert match(('star', ('lit', 'a')), 'aaabcd') == 'aaa'
    assert match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == None
    assert match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab') == 'a'
    assert search(('lit', ''), '') == ''
    assert search(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == 'b'
    assert matchset(('lit', 'abc'), 'abcdef')              == set(['def'])
    assert matchset(('seq', ('lit', 'hi '),
                     ('lit', 'there ')),
                   'hi there nice to meet you')            == set(['nice to meet you'])
    assert matchset(('alt', ('lit', 'dog'),
                    ('lit', 'cat')), 'dog and cat')        == set([' and cat'])
    assert (matchset(('dot', ), 'am i missing something?')
            == set(['m i missing something?']))
    assert matchset(('dot', ), '')                         == frozenset([])
    assert matchset(('oneof', 'a'), 'aabc123')             == set(['abc123'])
    assert matchset(('oneof', 'abc'), 'babc123')           == set(['abc123'])
    assert matchset(('oneof', 'abc'), 'dabc123')           == frozenset([])
    assert matchset(('eol', ), '')                         == set([''])
    assert matchset(('eol', ), 'not end of line')          == frozenset([])
    assert matchset(('star', ('lit', 'hey')), 'heyhey!') == set(['!', 'heyhey!', 'hey!'])

    assert lit('abc')         == ('lit', 'abc')
    assert seq(('lit', 'a'),
               ('lit', 'b'))  == ('seq', ('lit', 'a'), ('lit', 'b'))
    assert alt(('lit', 'a'),
               ('lit', 'b'))  == ('alt', ('lit', 'a'), ('lit', 'b'))
    assert star(('lit', 'a')) == ('star', ('lit', 'a'))
    assert plus(('lit', 'c')) == ('seq', ('lit', 'c'),
                                  ('star', ('lit', 'c')))
    assert opt(('lit', 'x'))  == ('alt', ('lit', ''), ('lit', 'x'))
    assert oneof('abc')       == ('oneof', ('a', 'b', 'c'))
    return 'tests pass'

if __name__ == '__main__':
    print test()
regex_compiler.py

def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key = len)
        return text[:len(text)-len(shortest)]

def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text) or 1):
        m = match(pattern, text[i:])
        if m is not None: return m

def lit(s): return lambda t: set([t[len(s):]]) if t.startswith(s) else null
def seq(x, y): return lambda t: set().union(*map(y, x(t)))
def alt(x, y): return lambda t: x(t) | y(t)
def oneof(chars): return lambda t: set([t[1:]]) if (t and t[0] in chars) else null
def opt(x): return lambda t: alt(lit(''), x)(t)

dot = lambda t: set([t[1:]]) if t else null
eol = lambda t: set(['']) if t == '' else null
def star(x): return lambda t: (set([t]) |
                               set(t2 for t1 in x(t) if t1 != t
                                   for t2 in star(x)(t1)))
def plus(x): return lambda t: seq(x, star(x))(t)

null = frozenset([])

def test():
    g = alt(lit('a'), lit('b'))
    assert g('abc') == set(['bc'])

    assert match(star(lit('a')), 'aaaaabbbaa') == 'aaaaa'
    assert match(lit('hello'), 'hello how are you?') == 'hello'
    assert match(lit('x'), 'hello how are you?') == None
    assert match(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
    assert match(oneof('xyz'), '   x is here!') == None

    assert match(star(lit('a')), 'aaabcd') == 'aaa'
    assert match(lit('abc'), 'abc') == 'abc'
    assert match(alt(lit('b'), lit('c')), 'ab') == None
    assert match(alt(lit('b'), lit('a')), 'ab') == 'a'
    assert search(lit(''), '') == ''
    assert search(alt(lit('b'), lit('c')), 'ab') == 'b'
    assert search(star(alt(lit('a'), lit('b'))), 'ab') == 'ab'
    assert search(alt(lit('b'), lit('c')), 'ad') == None
    assert lit('abc')('abcdef') == set(['def'])
    assert (seq(lit('hi '), lit('there '))('hi there nice to meet you')
            == set(['nice to meet you']))
    assert alt(lit('dog'), lit('cat'))('dog and cat') == set([' and cat'])
    assert dot('am i missing something?') == set(['m i missing something?'])
    assert dot('') == frozenset([])
    assert oneof('a')('aabc123') == set(['abc123'])
    assert oneof('abc')('babc123') == set(['abc123'])
    assert oneof('abc')('dabc123') == frozenset([])
    assert eol('') == set([''])
    assert eol('not end of line') == frozenset([])
    assert star(lit('hey'))('heyhey!') == set(['!', 'heyhey!', 'hey!'])
    assert plus(lit('hey'))('heyhey!') == set(['!', 'hey!'])
    assert opt(lit('hey'))('heyhey!') == set(['hey!', 'heyhey!'])

    return 'tests pass'

print test()
regex_generator.py

def lit(s):         return lambda Ns: set([s]) if len(s) in Ns else null
def alt(x, y):      return lambda Ns: x(Ns) | y(Ns)
def star(x):        return lambda Ns: opt(plus(x))(Ns)
def plus(x):        return lambda Ns: genseq(x, star(x), Ns, startx = 1) #Tricky
def oneof(chars):   return lambda Ns: set(chars) if 1 in Ns else null
def seq(x, y):      return lambda Ns: genseq(x, y, Ns)
def opt(x):         return alt(epsilon, x)
dot = oneof('?')    # You could expand the alphabet to more chars.
epsilon = lit('')   # The pattern that matches the empty string.

null = frozenset([])

def genseq(x, y, Ns, startx = 0):
    """Set of matches to xy whose total len is in Ns, with x-match's len in Ns and
    >= startx"""
    # Tricky part: x+ is defined as: x+ = x x* To stop the recursion, the first x
    # must generate at least 1 char, and then the recursive x* has that many fewer
    # characters. We use startx = 1 to say that x must match at least 1 character
    if not Ns:
        return null
    xmatches = x(set(range(startx, max(Ns)+1)))
    Ns_x = set(len(m) for m in xmatches)
    Ns_y = set(n-m for n in Ns for m in Ns_x if n-m >= 0)
    ymatches = y(Ns_y)
    return set(m1+m2 for m1 in xmatches for m2 in ymatches if len(m1+m2) in Ns)

def test():
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null

    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])

    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null
    return 'tests pass'

def test_gen():
    def N(hi):
        return set(range(hi+1))
    a, b, c = map(lit, 'abc')
    assert star(oneof('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b'])
    assert (seq(star(a), seq(star(b), star(c)))(set([4])) ==
            set(['aaaa', 'aaab', 'aaac', 'aabb', 'aabc', 'aacc', 'abbb',
                 'abbc', 'abcc', 'accc', 'bbbb', 'bbbc', 'bbcc', 'bccc', 'cccc']))
    assert (seq(plus(a), seq(plus(b), plus(c)))(set([5])) ==
            set(['aaabc', 'aabbc', 'aabcc', 'abbbc', 'abbcc', 'abccc']))
    assert (seq(oneof('bcfhrsm'), lit('at'))(N(3)) ==
            set(['bat', 'cat', 'fat', 'hat', 'mat', 'rat', 'sat']))
    assert (seq(star(alt(a, b)), opt(c))(set([3])) ==
            set(['aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'baa',
                 'bab', 'bac', 'bba', 'bbb', 'bbc']))
    assert lit('hello')(set([5])) == set(['hello'])
    assert lit('hello')(set([4])) == set()
    assert lit('hello')(set([6])) == set()
    return 'test_gen passes'

print(test())
print(test_gen())