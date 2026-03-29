import logging

logging.basicConfig(
    level=logging.WARNING,    # BUG: level is WARNING; DEBUG messages are suppressed
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def process(items):
    """Double each item, logging progress at DEBUG level."""
    logger.debug(f"Starting process() with {len(items)} items")   # BUG: never appears
    results = []
    for item in items:
        logger.debug(f"  processing item {item!r}")               # BUG: never appears
        results.append(item * 2)
    logger.debug(f"Finished: {len(results)} results")             # BUG: never appears
    return results


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    output = process(data)
    print(f"Output: {output}")
    print("(no debug messages shown — logger.debug() calls are silenced by WARNING level)")
    print(f"Effective log level: {logging.getLevelName(logger.getEffectiveLevel())}")
