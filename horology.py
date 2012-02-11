import math

def gregorian_to_julian(year, month, day):
    """Convert Gregorian date to Julian date.

    >>> gregorian_to_julian(2011, 12, 21)
    2455917
    """

    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3

    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

def julian_to_gregorian(JD):
    """Convert Julian date to Gregorian date.

    >>> julian_to_gregorian(2455916.5)
    (2011, 12, 21.0)
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

def julian_to_unix(jd):
    """Convert Julian Date to Unix time.
    """

    return (jd - 2440587.5) * 86400

def unix_to_julian(u):
    """Convert Unix time to Julian Date.

    >>> int(unix_to_julian(1324484390))
    2455917
    """

    return u / 86400. + 2440587.5

def sun_events(t, l_w, phi):
    """Return the times for sunrise, solar transit, and sunset.

    >>> map(int, sun_events(2455917, -10.756389, 59.949444))
    [2445911, 2460681, 2475451]
    """

    J_date = unix_to_julian(t)

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

    return tuple(map(julian_to_unix, [J_rise, J_transit, J_set]))

def lunar_phase(t):
    """Return the phase of the moon at UNIX time t.

    >>> lunar_phase(1328980430.472815)
    0.1302754907133155
    """

    lunar_period = 29.530588853 * 86400
    last_full_moon = 1328648040

    return ((t - last_full_moon) % lunar_period) / lunar_period

if __name__ == "__main__":
    import doctest
    failed, attempted = doctest.testmod()
    if False and failed == 0:
        print "Yay! All %d tests passed!" % attempted

    import time
    lon = -10.756389
    lat = 59.949444

    now = time.time()

    format = lambda t: time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(t))

    up, noon, down = sun_events(now, lon, lat)

    print "Now:             %s" % format(now)
    print "Sunrise:         %s" % format(up)
    print "Solar transit:   %s" % format(noon)
    print "Sunset:          %s" % format(down)
    print "Lunar phase:     %.1f%%" % lunar_phase(now)
