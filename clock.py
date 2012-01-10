#!/usr/bin/env python
#encoding=utf-8

from __future__ import division

from math import cos, sin, pi
import sys
import time

import pygame
from pygame import gfxdraw

import horology

tau = 2 * pi

lon = -10.756389
lat = 59.949444

day_colors = (0x00, 0x00, 0x00), (0xff, 0xff, 0xea)
night_colors = (0x00, 0x00, 0x00), (0xff, 0x00, 0x00)

bg, fg = day_colors

def artoxy(a, r, xo=0, yo=0):
    angle = tau * a - tau / 4
    x = xo + int(r * cos(angle))
    y = yo + int(r * sin(angle))

    return x, y

def draw_dial(dial):
    w, h = dial.get_size()

    dial.fill(bg)

    xo = w // 2
    yo = h // 2

    r = 0.3 * min(w, h)
    for i in range(1, 13):
        a = i / 12
        x, y = artoxy(a, r, xo, yo)

        label = hf.render("%d" % i, True, fg)
        lw, lh = label.get_size()

        dial.blit(label, (x - lw // 2, y - lh // 2))

    r = 0.4 * min(w, h)
    for i in range(5, 61, 5):
        a = i / 60
        b = -360 * a
        x, y = artoxy(a, r, xo, yo)

        label = mf.render("%d" % i, True, fg)
        label = pygame.transform.rotozoom(label, b, 1.0)
        lw, lh = label.get_size()

        dial.blit(label, (x - lw // 2, y - lh // 2))

def draw(screen, now):
    w, h = screen.get_size()

    sunrise, noon, sunset = [((t - time.timezone) / 3600) % 12 for t in horology.sun_events(now, lon, lat)]

    local_now = now - time.timezone
    minutes = (local_now / 60) % 60
    hours = (local_now / 3600) % 12

    draw_dial(screen)

    xo = w // 2
    yo = h // 2
    ro = 0.04 * min(w, h)

    a = hours / 12
    r = 0.22 * min(w, h)
    x, y = artoxy(a, r, xo, yo)

    points = (x, y), artoxy(a - 0.25, ro, xo, yo), artoxy(a + 0.25, ro, xo, yo)
    gfxdraw.filled_polygon(screen, points, fg)

    a = minutes / 60
    r *= 1.61803
    x, y = artoxy(a, r, xo, yo)

    points = (x, y), artoxy(a - 0.25, ro, xo, yo), artoxy(a + 0.25, ro, xo, yo)
    gfxdraw.filled_polygon(screen, points, fg)

    gfxdraw.filled_circle(screen, xo, yo, int(ro), fg)

    r = 0.25 * min(w, h)

    a = sunrise / 12
    x, y = artoxy(a, r, xo, yo)
    gfxdraw.filled_circle(screen, x, y, int(0.25 * ro), fg)

    a = sunset / 12
    x, y = artoxy(a, r, xo, yo)
    gfxdraw.filled_circle(screen, x, y, int(0.25 * ro), fg)

def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.time.set_timer(pygame.VIDEOEXPOSE, 5000)

    if "-f" in sys.argv:
        w, h = pygame.display.list_modes()[0]
        flags = pygame.FULLSCREEN
    else:
        w, h = 300, 300
        flags = 0

    screen = pygame.display.set_mode((w, h), flags)

    global hf, mf
    hf = pygame.font.SysFont("Dejavu Sans", 56)
    mf = pygame.font.SysFont("Dejavu Sans", 34)

    while True:
        event = pygame.event.wait()

        if event.type == pygame.VIDEOEXPOSE:
            now = time.time()
            draw(screen, now)
            pygame.display.update()

        elif event.type == pygame.VIDEORESIZE:
            w, h = event.w, event.h
            screen = pygame.display.set_mode((w, h), flags)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 0
            elif event.key == pygame.K_q:
                return 0
            elif event.key == pygame.K_d:
                global bg, fg
                bg, fg = day_colors
            elif event.key == pygame.K_n:
                global bg, fg
                bg, fg = night_colors

        elif event.type == pygame.QUIT:
            return 0

if __name__ == "__main__":
    sys.exit(main())
