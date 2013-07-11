def replace_if(x, in_, with_):
    if x in in_:
        return with_
    else:
        return x


def cycle(xs):
    i = 0
    length = len(xs)
    while True:
        yield xs[i % length]
        i += 1


def replace_alternating(ss, targets, reps):
    if reps:
        inf_reps = cycle(reps)
    else:
        inf_reps = cycle([''])

    result = [replace_if(s, targets, inf_reps.next()) for s in ss]
    return result


def fix_string(text, problems, corrections):
    return replace_alternating(text.split(), problems, corrections)
