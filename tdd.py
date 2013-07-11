from hypothesis.testdecorators import given
from hypothesis.statefultesting import requires, step, StatefulTest
from hypothesis.verifier import Unfalsifiable
from amazeballs import cycle, fix_string, replace_if, replace_alternating


def for_all_not_in(xs, in_, whitelist):
    wl = whitelist + ['']
    return all([(x not in in_) or (x in wl) for x in xs])


def get_from_gen(gen, i):
    for _ in range(i):
        gen.next()
    return gen.next()


@given(int, [int], [str])
def test_replace_if(x, y, z):
    assert replace_if(x, y, z) == (z if x in y else x)


@given([int])
def test_cycle(x):
    assert (not x) or \
        (get_from_gen(cycle(x), 0) == get_from_gen(cycle(x), len(x)))
    assert (not x) or \
        (get_from_gen(cycle(x), 1) ==
        get_from_gen(cycle(x), 2 + 2 * len(x)))


@given([str], [str], [str])
def test_replace_alternating(ss, ts, rs):
    assert for_all_not_in(ts, replace_alternating(ss, ts, rs), rs)


@given(str, [str], [str])
def test_fix_string(s, ps, cs):
    assert for_all_not_in(ps, fix_string(s, ps, cs), cs)


def test_stateful():
    try:
        example = ApplyMultiple().breaking_example()
        print example
        assert False
    except Unfalsifiable, e:
        assert True


class ApplyMultiple(StatefulTest):
    def __init__(self):
        self.target = "abc dere euege eueg A E O U I"

    @step
    @requires(str, str)
    def fix_one(self, problem, correction):
        self.target = fix_string(self.target, [problem], [correction])
        assert problem not in self.target or problem == correction
        self.target = " ".join(self.target)