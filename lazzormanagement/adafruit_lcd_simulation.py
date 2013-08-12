import pygame
import pygame.font
import threading
import sys
import time

from pygame.locals import *

class Adafruit_CharLCDPlate(object):
    
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    SELECT = 4

    def __init__(self):
        x = 160
        y = 32
        self.X = x
        self.Y = y
        pygame.init()

        self._screen = pygame.display.set_mode((x, y))
        self._screen.fill((0, 0, 0))
        pygame.display.set_caption(sys.argv[0])

        self._updatethread = threading.Thread(target=self._handle_events)
        self._updatethread.setDaemon(True)
        self._updatethread.start()
        self._pressed = 0
        self._color = (255, 255, 255)
        self._fontsize = 16
        self._font = pygame.font.SysFont("monospace", self._fontsize)

    def _check_key(self, pressed, index, mask):
        if pressed[index]:
            self._pressed |= (1 << mask)
        else:
            self._pressed &= ~(1 << mask)

    def _handle_events(self):
        while 1:
            event = pygame.event.wait()
            pressed = pygame.key.get_pressed()
            self._check_key(pressed, K_LEFT, self.LEFT)
            self._check_key(pressed, K_RIGHT, self.RIGHT)
            self._check_key(pressed, K_UP, self.UP)
            self._check_key(pressed, K_DOWN, self.DOWN)
            self._check_key(pressed, K_RETURN, self.SELECT)

            if event.type in (QUIT, QUIT):
                print event
                import os
                os.kill(os.getpid(), 9)

    def buttons(self):
        return self._pressed

    def update(self):
        surf = pygame.Surface((xsize,ysize))
        surf.fill(tuple(map(int, new)))
        screen.blit(surf, (x*xsize, y*ysize))
        pygame.display.update()

        surface = pygame.image.fromstring(data, size, mode)
        self.screen.blit(surface, (0,0))
        pygame.display.update()

    def begin(self, cols, rows):
        self._cols = cols
        self._rows = rows
        self.clear()

    def clear(self):
        self._data = [[' '] * self._cols for x in xrange(self._rows)]
        self._row = 0
        self._col = 0

    def set(self, character):
        try:
            self._data[self._row][self._col] = character
        except IndexError:
            pass
   
    def message(self, message):
        for character in message:
            if character == '\n':
                self._row += 1
                self._col = 0
                continue
            self.set(character)
            self._col += 1
        
        self._show()
 
    def _show(self):
        #print('+' + '-' * self._cols + '+')
        #for row in self._data:
        #    print('|' + ''.join(row) + '|')
        #print('+' + '-' * self._cols + '+')
        index = 0
        self._screen.fill((0, 0, 0))
        for row in self._data:
            text = self._font.render(''.join(row), False, self._color)
            self._screen.blit(text, (0, index))
            index += self._fontsize
        pygame.display.update()

    def setCursor(self, col, row):
        self._col = col
        self._row = row

