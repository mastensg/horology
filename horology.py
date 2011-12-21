import math

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

def julian_to_gregorian(JD):
    """Return the Gregorian calendar date from a Julian Day Number.

    >>> julian_to_gregorian(2455916.969553709)
    (2011, 12, 21.46955370903015)
    """

    J = JD + 0.5
    j = J + 32044

    g = j // 146097
    dg = j % 146097

    c = (dg // 36524 + 1) * 3 // 4
    dc = dg - c * 36524

    b = dc // 1461
    db = dc % 1461

    a = (db // 365 + 1) * 3 // 4
    da = db - a * 365

    y = g * 400 + c * 100 + b * 4 + a
    m = (da * 5 + 308) // 153 - 2
    d = da - (m + 4) * 153 // 5 + 122

    Y = int(y - 4800 + (m + 2) // 12)
    M = int((m + 2) % 12 + 1)
    D = d + 1

    return Y, M, D

def days_to_hms(days):
    """Return hours, minutes and seconds from days.

    >>> days_to_hms(0.46955370903)
    (12, 16, 9.440460192000549)
    """

    h = int(days * 24)
    m = int((days - h / 24.) * 24 * 60)
    s = (days - h / 24. - m / (24. * 60.)) * 24 * 60 * 60

    return h + 1, m, s

def sun_events(J_date, l_w, phi):
    """Return the Julian day times for sunrise, solar transit, and sunset.

    >>> sun_events(2455917, -10.756389, 59.949444)
    (0.32285522762686014, 0.46955370903015137, 0.6162521904334426)
    """

    acos = lambda x: math.degrees(math.acos(x))
    asin = lambda x: math.degrees(math.asin(x))

    cos = lambda x: math.cos(math.radians(x))
    sin = lambda x: math.sin(math.radians(x))

    # Calculate current Julian Cycle
    n_star = J_date - 2451545 - 0.0009 - l_w / 360.
    n = round(n_star)

    # Approximate Solar Noon
    J_star = 2451545 + 0.0009 + l_w / 360. + n

    # Solar Mean Anomaly
    M = (357.5291 + 0.98560028 * (J_star - 2451545)) % 360

    # Equation of Center
    C = 1.9148 * sin(M) + 0.0200 * sin(2 * M) + 0.0003 * sin(3 * M)

    # Ecliptic Longitude
    Lambda = (M + 102.9372 + C + 180) % 360

    # Solar Transit
    J_transit = J_star + (0.0053 * sin(M)) - (0.0069 * sin(2 * Lambda))

    # Declination of the Sun
    delta = asin(sin(Lambda) * sin(23.45))

    # Hour Angle
    omega_0 = acos((sin(-0.83) - sin(phi) * sin(delta)) / cos(phi) * cos(delta))

    # Calculate Sunrise and Sunset
    J_set = 2451545 + 0.0009 + ((omega_0 + l_w) / 360. + n + 0.0053 * sin(M)) - 0.0069 * sin(2 * Lambda)
    J_rise = J_transit - (J_set - J_transit)

    return tuple([j - J_date + 0.5 for j in J_rise, J_transit, J_set])

if __name__ == "__main__":
    import doctest
    failed, attempted = doctest.testmod()
    if failed == 0:
        print "Yay! All %d tests passed!" % attempted

    lon = -10.756389
    lat = 59.949444
    for i in range(7):
        jd = 2455917 + i
        up, noon, down = ["%02d:%02d:%02d" % days_to_hms(j) for j in sun_events(jd, lon, lat)]
        print "%d\t%s\t%s\t%s" % (i, up, noon, down)
