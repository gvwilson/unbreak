from datetime import datetime, timedelta


def add_days(start_str, days):
    """Return the wall-clock time `days` days after start_str (YYYY-MM-DD HH:MM)."""
    dt = datetime.fromisoformat(start_str)  # BUG: naive datetime strips timezone info;
    return dt + timedelta(days=days)        #      timedelta always adds exactly 86400s
                                            #      per day, ignoring DST transitions


if __name__ == "__main__":
    # 2024-03-10: US Eastern clocks spring forward at 02:00 (a 23-hour day).
    # A job that was run at 2024-03-09 08:00 and should repeat "one day later"
    # should fire at 08:00 EDT on 2024-03-10 — but that is only 23 hours away.

    start = "2024-03-09 08:00"
    result = add_days(start, days=1)

    print(f"Start:          {start}  (America/New_York, pre-DST)")
    print(f"+ 1 naive day:  {result}")
    print()
    print("The naive result is 2024-03-10 08:00, which looks correct.")
    print("But clocks sprang forward at 02:00, so only 23 hours elapsed.")
    print("A timezone-aware calculation using zoneinfo or pytz would show")
    print("the gap and let you choose: 23 wall-clock hours or 24 absolute hours.")
    print()

    # Show what UTC-based arithmetic reveals
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("America/New_York")
        aware = datetime(2024, 3, 9, 8, 0, tzinfo=tz)
        print(f"Aware start UTC offset: {aware.utcoffset()}  ({aware.tzname()})")
        result_aware = aware + timedelta(days=1)
        print(f"Aware result UTC offset: {result_aware.utcoffset()}  ({result_aware.tzname()})")
        utc_hours = (result_aware.utctimetuple(), aware.utctimetuple())
        import calendar
        start_utc = calendar.timegm(aware.utctimetuple())
        end_utc = calendar.timegm(result_aware.utctimetuple())
        print(f"Actual elapsed seconds: {end_utc - start_utc}  "
              f"(86400 = 24h; 82800 = 23h)")
    except ImportError:
        print("Install Python 3.9+ for zoneinfo demonstration")
