def gregorian_to_julian(year, month, day):
    """Return the Julian Day Number from a Gregorian calendar date.

    >>> gregorian_to_julian(2011, 12, 21)
    2455917
    """

    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3

    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

def unix_to_julian(U):
    """Return the Julian Day Number from seconds since the UNIX epoch.

    >>> unix_to_julian(1324484390)
    2455917
    """

    ss = U % 60
    a = (U - ss) // 60
    mm = a % 60
    b = (a - mm) // 60
    hh = b % 24
    u = U - ss - mm * 60 - hh * 3600

    return u // 86400 + 2440588

if __name__ == "__main__":
    import doctest
    failed, attempted = doctest.testmod()
    if failed == 0:
        print "Yay! All %d tests passed!" % attempted
