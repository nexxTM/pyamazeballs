from hypothesis import falsify
from hypothesis.statefultesting import requires, step, StatefulTest
from hypothesis.searchstrategy import SearchStrategy, strategy_for
from random import randint
from amazeballs import cycle, fix_string, replace_if, replace_alternating


def for_all_not_in(xs, in_, whitelist):
    wl = whitelist + ['']
    return all([(x not in in_) or (x in wl) for x in xs])


def get_from_gen(gen, i):
    for _ in range(i):
        gen.next()
    return gen.next()


def my_falsify(name, *args):
    print name + ": "
    try:
        print falsify(*args)
    except Exception, e:
        print e


def implies(a, b):
    """
    The logical implication (a => b)
    (not a) or b
    """

    if a:
        return b
    else:
        return True


def implies_lazy(a, f):
    """
    The logical implication (a => b)

    The second argument has to be a function.
    It will be lazily evaluated if needed.

    (not a) or b
    """

    if a:
        return f()
    else:
        return True


my_falsify("replace if",
           lambda x, y, z: replace_if(x, y, z) == (z if x in y else x),
            int, [int], str)


def replace_if_prop(x, y, z):
    return replace_if(x, y, z) == (z if x in y else x)

my_falsify("replace if2", replace_if_prop, int, [int], str)

my_falsify("replace alternating",
           lambda ss, ts, rs:
                for_all_not_in(ts, replace_alternating(ss, ts, rs), rs),
            [str], [str], [str])

my_falsify("cycle1", lambda x: (not x) or
                (get_from_gen(cycle(x), 0) == get_from_gen(cycle(x), len(x))),
           [int])

my_falsify("cycle false", lambda x: (not x) or
                (get_from_gen(cycle(x), 1) ==
                 get_from_gen(cycle(x), 2 + 2 * len(x))),
           # +1 would be correct
           [int])

my_falsify("strict evaluation", lambda x: implies(x,
                (get_from_gen(cycle(x), 0) == get_from_gen(cycle(x), len(x)))),
           [int])

my_falsify("lazy implies", lambda x: implies(x, lambda:
                (get_from_gen(cycle(x), 0) == get_from_gen(cycle(x), len(x)))),
           [int])

my_falsify("fix string", lambda s, ps, cs:
                for_all_not_in(ps, fix_string(s, ps, cs), cs),
           str, [str], [str])


class MyInt(int):

    def __new__(cls, v):
        return super(MyInt, cls).__new__(cls, v)


@strategy_for(MyInt)
class MyIntStrategy(SearchStrategy):
    # simplified
    def produce(self, size, flags):
        return MyInt(randint(-2 ** 5, 2 ** 5))

my_falsify("MyInt", lambda x: (not x) or
                (get_from_gen(cycle(x), 1) == get_from_gen(cycle(x), len(x))),
           [MyInt])


class ApplyMultiple(StatefulTest):
    def __init__(self):
        self.target = "abc dere euege eueg A E O U I"

    @step
    @requires(str, str)
    def fix_one(self, problem, correction):
        self.target = fix_string(self.target, [problem], [correction])
        assert problem not in self.target or problem == correction
        self.target = " ".join(self.target)

try:
    print ApplyMultiple().breaking_example()
except Exception, e:
    print e
