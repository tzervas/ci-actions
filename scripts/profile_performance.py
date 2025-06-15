import cProfile
import pstats
import sys


def profile_application(script):
    profiler = cProfile.Profile()
    profiler.enable()
    exec(open(script).read())
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumtime").print_stats(10)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python profile_performance.py <script.py>")
        sys.exit(1)
    profile_application(sys.argv[1])
