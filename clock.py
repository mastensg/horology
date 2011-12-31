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

def artoxy(a, r, xo=0, yo=0):
    angle = tau * a - tau / 4
    x = xo + int(r * cos(angle))
    y = yo + int(r * sin(angle))

    return x, y

def draw_dial(dial):
    w, h = dial.get_size()

    fg = 0xff, 0xff, 0xea
    bg = 0x00, 0x00, 0x00

    dial.fill(bg)

    xo = w // 2
    yo = h // 2

    r = 0.3 * min(sw, sh)
    for i in range(1, 13):
        a = i / 12
        x, y = artoxy(a, r, xo, yo)

        label = hf.render("%d" % i, True, fg)
        lw, lh = label.get_size()

        dial.blit(label, (x - lw // 2, y - lh // 2))

    r = 0.4 * min(sw, sh)
    for i in range(5, 61, 5):
        a = i / 60
        b = -360 * a
        x, y = artoxy(a, r, xo, yo)

        label = mf.render("%d" % i, True, fg)
        label = pygame.transform.rotate(label, b)
        lw, lh = label.get_size()

        dial.blit(label, (x - lw // 2, y - lh // 2))

def draw(screen, now):
    w, h = screen.get_size()

    jdn = horology.unix_to_julian(now) + 1
    sunrise, noon, sunset = horology.sun_events(jdn, lon, lat)
    seconds = now % 60
    minutes = (now / 60) % 60
    hours = (now / 3600) % 12
    #print int(hours), int(minutes), seconds

    draw_dial(screen)

    fg = 0xff, 0xff, 0xea
    bg = 0x00, 0x00, 0x00

    xo = w // 2
    yo = h // 2

    a = hours / 12
    r = 0.25 * min(sw, sh)
    x, y = artoxy(a, r, xo, yo)

    points = (x, y), artoxy(a - 0.25, 0.2 * r, xo, yo), artoxy(a + 0.25, 0.2 * r, xo, yo)
    gfxdraw.filled_polygon(screen, points, fg)

    a = minutes / 60
    r = 0.38 * min(sw, sh)
    x, y = artoxy(a, r, xo, yo)

    points = (x, y), artoxy(a - 0.25, 0.1 * r, xo, yo), artoxy(a + 0.25, 0.1 * r, xo, yo)
    gfxdraw.filled_polygon(screen, points, fg)

    a = seconds / 60
    r = 0.38 * min(sw, sh)
    x, y = artoxy(a, r, xo, yo)

    gfxdraw.filled_circle(screen, xo, yo, int(0.05 * min(sw, sh)), fg)

def main():
    pygame.init()

    pygame.mouse.set_visible(False)

    framerate = 1
    pygame.time.set_timer(pygame.VIDEOEXPOSE, 1000 // framerate)

    global sw, sh
    sw, sh = 800, 480
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
    screen = pygame.display.set_mode((sw, sh), flags)

    global hf, mf
    hf = pygame.font.SysFont("Dejavu Sans", 56)
    mf = pygame.font.SysFont("Dejavu Sans", 24)

    tz = 3600
    while True:
        now = time.time() + tz
        draw(screen, now)
        pygame.display.update()
        time.sleep(3)
    exit()
    while True:
        event = pygame.event.wait()

        if event.type == pygame.VIDEOEXPOSE:
            now = time.time()
            draw(screen, now)
            pygame.display.update()

        elif event.type == pygame.VIDEORESIZE:
            sw, sh = event.w, event.h
            screen = pygame.display.set_mode((sw, sh), flags)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 0

        elif event.type == pygame.QUIT:
            return 0

if __name__ == "__main__":
    sys.exit(main())
