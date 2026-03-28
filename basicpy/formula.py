def dms_to_decimal(degrees, minutes, seconds):
    """Convert degrees/minutes/seconds to decimal degrees."""
    return degrees + minutes / 60 + seconds / 60  # BUG: seconds should be divided by 3600


if __name__ == "__main__":
    tests = [
        (1, 30, 0,    1.5),   # 1°30'0"  = 1.5°
        (0, 0,  3600, 1.0),   # 0°0'3600" = 1.0°
        (45, 15, 30,  45.2583333),
    ]
    for deg, mins, secs, expected in tests:
        result = dms_to_decimal(deg, mins, secs)
        print(f"{deg}°{mins}'{secs}\" = {result:.7f}  (expected {expected})")
