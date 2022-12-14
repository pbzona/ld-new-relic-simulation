from datetime import datetime, timedelta
from random import randint, choice
import string
from launchdarkly.client import LDClient
from simulation.config import MEMORY_MB_MAX, MEMORY_MB_MIN, MEMORY_TIME_MAX, MEMORY_TIME_MIN

# Increases memory usage arbitrarily to illustrate changes to memory as a performance metric
def increase_memory_usage(ctx):
    ld = LDClient.get_instance()
    usage_in_mb = randint(MEMORY_MB_MIN, MEMORY_MB_MAX)
    duration_seconds = randint(MEMORY_TIME_MIN, MEMORY_TIME_MAX)

    # Boolean indicating whether the memory increase should be applied
    memory_spiked = ld.variation('memory-intensive-feature', ctx, False)

    # Generate a different random char each time to ensure built in optimizations
    # don't come into effect and reduce memory usage
    random_char = choice(string.ascii_letters)

    # Allocates a number of MB of memory, multiplied by a constant if flag is on
    if memory_spiked:
        # Factor by which to increase memory usage
        increase_factor = ld.variation('memory-increase-factor', ctx, 3)

        memory = random_char * 1024 * 1024 * usage_in_mb * increase_factor
    else:
        memory = random_char * 1024 * 1024 * usage_in_mb

    # Keep the memory active, basically just waste time
    start = datetime.now()
    j = 0
    while (datetime.now() - start) < timedelta(seconds=duration_seconds):
        j += 1

    return usage_in_mb * increase_factor if memory_spiked else usage_in_mb