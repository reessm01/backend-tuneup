#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = "Scott Reese"

import cProfile
import pstats
import functools
import timeit
from functools import wraps
from collections import Counter


def profile(func):
    """A function that can be used as a decorator to measure performance"""
    @wraps(func)
    def inner_wrapper(*args, **kwargs):
        import cProfile
        import pstats
        import StringIO
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        s = StringIO.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
        ps.print_stats()
        print(s.getvalue())
        return result
    return inner_wrapper


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        line = f.readline()
        return f.read().splitlines()


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    counts = Counter(movies)
    return list(dict.fromkeys([movie for movie in movies if counts[movie] > 1]))


def timeit_helper():
    """Part A:  Obtain some profiling measurements using timeit"""
    t = timeit.Timer("main()", "from __main__ import main")
    times = t.repeat(repeat=7, number=5)
    res = [time/5 for time in times]
    print("Best time across 7 repeats of 5 runs per repeat: " +
          str(min(res)) + " sec")


def main():
    """Computes a list of duplicate movie entries"""
    result = find_duplicate_movies('movies.txt')
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))


if __name__ == '__main__':
    main()
