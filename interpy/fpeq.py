def running_total(amounts):
    """Return the total by accumulating amounts one at a time."""
    result = 0.0
    for a in amounts:
        result += a
    return result


def direct_total(amounts):
    """Return the total by summing all amounts at once."""
    return sum(amounts)


if __name__ == "__main__":
    # 0.1 cannot be represented exactly in binary floating point;
    # accumulating it in different orders produces different rounding errors.
    amounts = [0.1] * 10   # mathematically equals 1.0

    t1 = running_total(amounts)
    t2 = direct_total(amounts)

    print(f"Running total: {t1!r}")
    print(f"Direct total:  {t2!r}")

    if t1 == 1.0:   # BUG: == on floats; should use math.isclose(t1, 1.0)
        print("Running total is exactly 1.0")
    else:
        print(f"Running total is NOT exactly 1.0 (off by {abs(t1 - 1.0)!r})")

    if t1 == t2:    # BUG: two routes to the same value may not compare equal
        print("Totals match.")
    else:
        print("Totals differ!")
