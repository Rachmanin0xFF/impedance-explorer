import pstats
from pstats import SortKey

def show_stats(path):
    p = pstats.Stats(path)
    p.sort_stats(SortKey.CUMULATIVE).print_stats(10)

def get_stat(path):
    p = pstats.Stats(path)
    return p.total_tt