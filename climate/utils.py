# Utility

import cProfile
import os
import pstats


def profile(x, n=10):
    """Profile code using cProfile"""
    tf = "MUR09HJUAS0GL0TDB7M9.txt"
    try:
        cProfile.run(x, tf)
        p = pstats.Stats(tf)
    finally:
        os.remove(tf)
    p.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_callees(n)

