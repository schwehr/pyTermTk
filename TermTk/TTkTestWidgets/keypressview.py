#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from signal import raise_signal
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent, mod2str, key2str
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.timer import TTkTimer
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget

class TTkKeyPressView(TTkWidget):
    __slots__ = ('_timer','_keys','_fade','_period')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = kwargs.get('name' , 'TTkAbstractScrollView')
        TTkHelper._rootWidget.eventKeyPress.connect(self._addKey)
        self._keys = []
        self._period = 0.2
        self._fade = 5
        self._timer = TTkTimer()
        self._timer.timeout.connect(self._timerEvent)
        self._timer.start(self._period)

    @pyTTkSlot(TTkKeyEvent)
    def _addKey(self, evt):
        if evt.type == TTkK.Character:
            text = evt.key
        else:
            text = key2str(evt.key).replace("Key_",'')
            if evt.mod:
                m = mod2str(evt.mod).replace("Modifier",'')
                text = f"{m} {text}"
        if self._keys and evt.type == self._keys[-1][2] == TTkK.Character:
             self._keys[-1][1]+=evt.key
             self._keys[-1][0]=0
        else:
            self._keys.append([0,text,evt.type])
        self.update()

    def _timerEvent(self):
        for i,k in enumerate(self._keys):
            if k[0] > self._fade:
                self._keys.pop(i)
            else:
                k[0] += 1
        self.update()
        self._timer.start(self._period)

    def txt2map(self, txt):
        ret = ["","",""]
        for c in txt:
            m = self.fontMap.get(c,["...",". .","..."])
            ret[0] += m[0]
            ret[1] += m[1]
            ret[2] += m[2]
        return ret

    def paintEvent(self):
        for k in self._keys:
            text = k[1]
            gr = 0x1000 - 0x1000 * k[0] // self._fade
            r = 0xbb*gr//0x1000
            g = 0xff*gr//0x1000
            b = 0xff*gr//0x1000
            color = TTkColor.fg(f"#{r<<16|g<<8|b:06x}")
            #self._canvas.drawText(pos=((self.width()-len(text))//2,0),text=text,color=color)
            m = self.txt2map(text)
            self._canvas.drawText(pos=((self.width()-len(text)*3)//2,0),text=m[0],color=color)
            self._canvas.drawText(pos=((self.width()-len(text)*3)//2,1),text=m[1],color=color)
            self._canvas.drawText(pos=((self.width()-len(text)*3)//2,2),text=m[2],color=color)

    fontMap = {
        ' ':[
          "   ",
          "   ",
          "   ",
            ],
        '!':[
          " ▌ ",
          " ▘ ",
          " ▘ ",
            ],
        '\'':[
          " ▌ ",
          "   ",
          "   ",
            ],
        '"':[
          "▐▐ ",
          "   ",
          "   ",
            ],
        '#':[
          "▟▟▖",
          "▟▟▖",
          "▝▝ ",
            ],
        '$':[
          "▞▛▘",
          "▝▛▖",
          "▀▀ ",
            ],
        '%':[
          "█▗▘",
          "▗▚▖",
          "▘▝▘",
            ],
        '&':[
          "▗▀ ",
          "▗▚ ",
          "▝▘▘",
            ],
        '(':[
          " ▞ ",
          " ▌ ",
          " ▝ ",
            ],
        ')':[
          "▝▖ ",
          " ▌ ",
          "▝  ",
            ],
        '*':[
          "▝▞ ",
          "▝▝ ",
          "   ",
            ],
        '+':[
          " ▖ ",
          "▝▛ ",
          "   ",
            ],
        ',':[
          "   ",
          " ▖ ",
          "▝  ",
            ],
        '-':[
          "   ",
          "▝▀ ",
          "   ",
            ],
        '.':[
          "   ",
          "   ",
          "▝  ",
            ],
        '/':[
          " ▗▘",
          "▗▘ ",
          "▘  ",
            ],
        '0':[
          "▛▀▌",
          "▌▘▌",
          "▀▀▘",
            ],
        '1':[
          "▗▌ ",
          " ▌ ",
          "▝▀ ",
            ],
        '2':[
          "▞▚ ",
          "▗▘ ",
          "▀▀ ",
            ],
        '3':[
          "▞▚ ",
          "▖▚ ",
          "▝▘ ",
            ],
        '4':[
          " ▞ ",
          "▟▄ ",
          " ▘ ",
            ],
        '5':[
          "▛▀▘",
          "▀▀▖",
          "▀▀ ",
            ],
        '6':[
          "▞▀ ",
          "▛▀▖",
          "▝▀ ",
            ],
        '7':[
          "▀▜▘",
          "▗▘ ",
          "▘  ",
            ],
        '8':[
          "▞▀▖",
          "▞▀▖",
          "▝▀ ",
            ],
        '9':[
          "▞▀▖",
          "▝▀▌",
          "▝▀ ",
            ],
        ':':[
          " ▖ ",
          " ▖ ",
          "   ",
            ],
        ';':[
          " ▖ ",
          " ▖ ",
          "▝  ",
            ],
        '<':[
          "▗▞▘",
          "▚▖ ",
          " ▝▘",
            ],
        '=':[
          "▄▄▖",
          "▄▄▖",
          "   ",
            ],
        '>':[
          "▀▄ ",
          " ▄▘",
          "▀  ",
            ],
        '?':[
          " ▚ ",
          " ▘ ",
          " ▘ ",
            ],
        '@':[
          "▞▛▖",
          "▌▀ ",
          "▝▘ ",
            ],
        'A':[
          "▞▀▖",
          "▛▀▌",
          "▘ ▘",
            ],
        'B':[
          "▛▀▖",
          "▛▀▖",
          "▀▀ ",
            ],
        'C':[
          "▞▀▘",
          "▌  ",
          "▝▀▘",
            ],
        'D':[
          "▛▀▖",
          "▌ ▌",
          "▀▀ ",
            ],
        'E':[
          "▛▀▘",
          "▛▀▘",
          "▀▀▘",
            ],
        'F':[
          "▛▀▘",
          "▛▀ ",
          "▘  ",
            ],
        'G':[
          "▛▀▘",
          "▌▝▌",
          "▀▀▘",
            ],
        'H':[
          "▌ ▌",
          "▛▀▌",
          "▘ ▘",
            ],
        'I':[
          "▝▛ ",
          " ▌ ",
          "▝▀ ",
            ],
        'J':[
          " ▜▘",
          "▖▐ ",
          "▝▘ ",
            ],
        'K':[
          "▌▞ ",
          "▛▖ ",
          "▘▝ ",
            ],
        'L':[
          "▌  ",
          "▌  ",
          "▀▀▘",
            ],
        'M':[
          "▙▗▌",
          "▌▘▌",
          "▘ ▘",
            ],
        'N':[
          "▙ ▌",
          "▌▚▌",
          "▘ ▘",
            ],
        'O':[
          "▞▀▖",
          "▌ ▌",
          "▝▀ ",
            ],
        'P':[
          "▛▀▖",
          "▛▀ ",
          "▘  ",
            ],
        'Q':[
          "▞▀▖",
          "▌▗▘",
          "▝▘▘",
            ],
        'R':[
          "▛▀▖",
          "▛▛ ",
          "▘▝ ",
            ],
        'S':[
          "▞▀▘",
          "▝▀▖",
          "▀▀ ",
            ],
        'T':[
          "▀▛▘",
          " ▌ ",
          " ▘ ",
            ],
        'U':[
          "▌ ▌",
          "▌ ▌",
          "▝▀ ",
            ],
        'V':[
          "▌ ▌",
          "▚▗▘",
          " ▘ ",
            ],
        'W':[
          "▌ ▌",
          "▌▖▌",
          "▝▀ ",
            ],
        'X':[
          "▚▗▘",
          "▗▚ ",
          "▘ ▘",
            ],
        'Y':[
          "▚▗▘",
          " ▌ ",
          " ▘ ",
            ],
        'Z':[
          "▀▜▘",
          "▗▘ ",
          "▀▀▘",
            ],
        '[':[
          " ▛ ",
          " ▌ ",
          " ▀ ",
            ],
        '\\':[
          "▚  ",
          " ▚ ",
          "  ▘",
            ],
        ']':[
          "▝▌ ",
          " ▌ ",
          "▝▘ ",
            ],
        '^':[
          "▗▚ ",
          "   ",
          "   ",
            ],
        '_':[
          "   ",
          "   ",
          "▀▀▘",
            ],
        '`':[
          "▝▖ ",
          "   ",
          "   ",
            ],
        'a':[
          "▗▖ ",
          "▌▐ ",
          "▝▘▘",
            ],
        'b':[
          "▐▄ ",
          "▐ ▌",
          " ▀ ",
            ],
        'c':[
          " ▄ ",
          "▐  ",
          " ▀ ",
            ],
        'd':[
          "▗▟ ",
          "▌▐ ",
          "▝▘ ",
            ],
        'e':[
          "▗▖ ",
          "▛▀ ",
          "▝▘ ",
            ],
        'f':[
          "▗▀ ",
          "▐▘ ",
          "▝  ",
            ],
        'g':[
          "▗▜ ",
          " ▜ ",
          " ▘ ",
            ],
        'h':[
          "▐  ",
          "▐▀▖",
          "▝ ▘",
            ],
        'i':[
          " ▖ ",
          " ▖ ",
          " ▘ ",
            ],
        'j':[
          " ▘ ",
          " ▌ ",
          "▝  ",
            ],
        'k':[
          "▗  ",
          "▐▞ ",
          "▝▝ ",
            ],
        'l':[
          "▗  ",
          "▐  ",
          " ▘ ",
            ],
        'm':[
          "▄▗ ",
          "▌▘▌",
          "▘ ▘",
            ],
        'n':[
          "▄▖ ",
          "▌▐ ",
          "▘▝ ",
            ],
        'o':[
          " ▄ ",
          "▐ ▌",
          " ▀ ",
            ],
        'p':[
          "▗▖ ",
          "▐▞ ",
          "▝  ",
            ],
        'q':[
          " ▄ ",
          "▝▟ ",
          " ▝ ",
            ],
        'r':[
          "   ",
          "▗▀ ",
          "▝  ",
            ],
        's':[
          "▗▄ ",
          "▝▙ ",
          "▝▀ ",
            ],
        't':[
          " ▖ ",
          "▝▛ ",
          " ▀ ",
            ],
        'u':[
          "   ",
          "▐▐ ",
          "▝▀ ",
            ],
        'v':[
          "   ",
          "▐▐ ",
          " ▘ ",
            ],
        'w':[
          "   ",
          "▌▖▌",
          "▝▀ ",
            ],
        'x':[
          "   ",
          "▝▞ ",
          "▝▝ ",
            ],
        'y':[
          "▗▗ ",
          "▝▞ ",
          "▝  ",
            ],
        'z':[
          "▗▄ ",
          "▗▛ ",
          "▝▀ ",
            ],
        '~':[
          "▗  ",
          "▘▚▘",
          "   ",
            ],
    }
