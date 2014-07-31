#!/user/bin/env python
"""
PyCLIE
(Python Command Line Interface Engine)
cli.py

http://pyclie.toofifty.me/
"""

# Libs
import traceback
import os
import time
import sys
import msvcrt
from threading import Thread
from colorama import init, Fore, Back
init()

# Internal
from color import Colors as c

FRAME_RATE = 10.0
LARGER_WIDTH = False

symbol_colors = {
    '#' : Fore.RED,
    chr(219) : Fore.CYAN,
    '.' : Fore.BLUE,
    'default' : Fore.WHITE,
}

def load_level(name):
    try:
        path = os.path.join('../levels/' + name + '.cll')
        with open(path, 'r') as level_file:
            level_array = []
            [level_array.append(piece) for piece in level_file.read()]
            return level_array
    except IOError:
        return False
    except:
        traceback.print_exc()
        
def draw_level(array):
    t = time.time()
    out = ''
    current_color = None
    for char in array:
        if char in symbol_colors:
            if current_color is not symbol_colors[char]:
                out += symbol_colors[char] + char
                current_color = symbol_colors[char]
            else:
                out += char
        else:
            if current_color is not Fore.WHITE:
                out += Fore.WHITE + char
                current_color = Fore.WHITE
            else:
                out += char
    print out + symbol_colors['default']
    return (time.time() - t)
    
class SceneRenderer(Thread):    
    def __init__(self, initial_array):
        Thread.__init__(self)
        self.level_array = initial_array
        self.running = True
        self.level_update = True
        
    def run(self):
        temp_time = time.time()
        while self.running:
            if self.level_update:
                os.system('cls')
                print 'PyCLIE v0.0.2a'
                delta_time = draw_level(self.level_array)
                try:
                    cycle_time = time.time() - temp_time
                    print 'Frame render:', '%.2f' % (delta_time*1000) + 'ms',
                    print '| PFPS:', '%.2f' % (1/delta_time),
                    print '| TFPS: ', '%.2f' % (1/(cycle_time)),
                    print '| Cycle time:', '%.2f' % (cycle_time*1000) + 'ms'
                except ZeroDivisionError:
                    continue
                except:
                    traceback.print_exc()
                self.level_update = False
            else:
                time.sleep(1.0 / FRAME_RATE)
            temp_time = time.time()
            
    def update_level(self, new_array):
        self.level_array = new_array
        self.level_update = True
        return self.level_array
        
    def close(self):
        self.running = False
        return not self.running
        
class Char:
    old_pos = [0, 0]

    def __init__(self, char, pos=[40, 10]):
        self.char = char
        self.pos = pos
        
    def move(self, am, dir):
        self.old_pos = self.pos[:]
        
        if dir == 0:
            self.pos[0] += am
        elif dir == 1:
            self.pos[1] += am
        elif dir == 2:
            self.pos[0] -= am
        elif dir == 3:
            self.pos[1] -= am
        return self.pos
        
    def set_pos(self, pos=[40,10]):
        self.pos = pos
        
def move_char(char, level_scene, level_array):
    new_ord = char.pos[1] * 80 + char.pos[0]
    old_ord = char.old_pos[1] * 80 + char.old_pos[0]
    level_scene[old_ord] = level_array[old_ord]
    level_scene[new_ord] = char.char
    return level_scene
    
def accept_input(c, nl, l):
    accepting_input = True
    while accepting_input:
        try:
            getch = msvcrt.getch().encode('hex')
            if getch == '48': # up
                ch.move(1, 3)
                nl = sr.update_level(move_char(ch, nl, l))
            elif getch == '4d': # right
                ch.move(1, 0)
                nl = sr.update_level(move_char(ch, nl, l))
            elif getch == '4b': # left
                ch.move(1, 2)
                nl = sr.update_level(move_char(ch, nl, l))
            elif getch == '50': # down
                ch.move(1, 1)   
                nl = sr.update_level(move_char(ch, nl, l))
            elif getch == '1b': # esc
                accepting_input = False
        except:
            traceback.print_exc()
        
if __name__ == '__main__':
    l = load_level('basic')
    l2 = load_level('basic2')
    ch = Char(chr(219), [40, 10])
    nl = l[:]
    nl = move_char(ch, nl, l)
    sr = SceneRenderer(l)
    sr.start()
    accept_input(ch, nl, l)    
    sr.close()
    
    
    
    
    
    
    