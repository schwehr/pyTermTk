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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper

# Ansi Escape Codes:
# https://conemu.github.io/en/AnsiEscapeCodes.html

# From http://pueblo.sourceforge.net/doc/manual/ansi_color_codes.html
# Code:         Client:   Meaning:
# [0m           --        reset; clears all colors and styles (to white on black)
# [1m           --        bold on (see below)
# [3m           --        italics on
# [4m           --        underline on
# [7m           2.50      inverse on; reverses foreground & background colors
# [9m           2.50      strikethrough on
# [22m          2.50      bold off (see below)
# [23m          2.50      italics off
# [24m          2.50      underline off
# [27m          2.50      inverse off
# [29m          2.50      strikethrough off
# [30m          --        set foreground color to black
# [31m          --        set foreground color to red
# [32m          --        set foreground color to green
# [33m          --        set foreground color to yellow
# [34m          --        set foreground color to blue
# [35m          --        set foreground color to magenta (purple)
# [36m          --        set foreground color to cyan
# [37m          --        set foreground color to white
# [39m          2.53      set foreground color to default (white)
# [40m          --        set background color to black
# [41m          --        set background color to red
# [42m          --        set background color to green
# [43m          --        set background color to yellow
# [44m          --        set background color to blue
# [45m          --        set background color to magenta (purple)
# [46m          --        set background color to cyan
# [47m          --        set background color to white
# [49m          2.53      set background color to default (black)

class _TTkColor:
    __slots__ = ('_fg','_bg','_mod', '_colorMod', '_buffer', '_clean')
    _fg: tuple; _bg: tuple; _mod: int
    def __init__(self, fg:tuple=None, bg:tuple=None, mod:int=0, colorMod=None, clean=False):
        self._fg  = fg
        self._bg  = bg
        self._mod = mod
        self._clean = clean or not (fg or bg or mod)
        self._colorMod = colorMod
        self._buffer = None

    def foreground(self):
        if self._fg:
            return _TTkColor(fg=self._fg)
        else:
            return None

    def background(self):
        if self._bg:
            return _TTkColor(bg=self._bg)
        else:
            return None

    def bold(self) -> bool:
        return  self._mod & TTkHelper.Color.BOLD

    def italic(self) -> bool:
        return  self._mod & TTkHelper.Color.ITALIC

    def underline(self) -> bool:
        return  self._mod & TTkHelper.Color.UNDERLINE

    def strikethrough(self) -> bool:
        return  self._mod & TTkHelper.Color.STRIKETROUGH

    def blinking(self) -> bool:
        return  self._mod & TTkHelper.Color.BLINKING

    def colorType(self):
        return \
            ( TTkK.Foreground if self._fg  else TTkK.NONE ) | \
            ( TTkK.Background if self._bg  else TTkK.NONE ) | \
            ( TTkK.Modifier   if self._mod else TTkK.NONE )

    def getHex(self, ctype):
        if ctype == TTkK.Foreground:
            r,g,b = self.fgToRGB()
        else:
            r,g,b = self.bgToRGB()
        return f"#{r<<16|g<<8|b:06x}"

    def fgToRGB(self):
        return self._fg if self._fg else (0,0,0)

    def bgToRGB(self):
        return self._bg if self._bg else (0,0,0)

    def invertFgBg(self):
        ret = self.copy()
        ret._fg = self._bg
        ret._bg = self._fg
        return ret

    def __str__(self):
        if not self._buffer:
            self._buffer = TTkHelper.Color.rgb2ansi(self._fg,self._bg,self._mod,self._clean)
        return self._buffer

    def __eq__(self, other):
        if other is None: return False
        return \
            self._fg  == other._fg and \
            self._bg  == other._bg and \
            self._mod == other._mod

    # self + other
    def __add__(self, other):
        # TTkLog.debug("__add__")
        if other._clean:
            return other.copy()
        clean = self._clean
        fg:  str = other._fg or self._fg
        bg:  str = other._bg or self._bg
        mod: str = self._mod + other._mod
        colorMod = other._colorMod or self._colorMod
        return TTkColor(fg,bg,mod,colorMod,clean)

    def __sub__(self, other):
        # TTkLog.debug("__sub__")
        # if other is None: return str(self)
        if ( None == self._bg  != other._bg  or
             None == self._fg  != other._fg  or
                     self._mod != other._mod ):
            ret = self.copy()
            ret._clean = True
            return ret
        return self

    def modParam(self, *args, **kwargs):
        if not self._colorMod: return self
        ret = self.copy()
        ret._colorMod.setParam(*args, **kwargs)
        return ret

    def mod(self, x , y):
        if self._colorMod is None: return self
        return self._colorMod.exec(x,y,self)

    def copy(self, modifier=True):
        ret = _TTkColor()
        ret._fg   = self._fg
        ret._bg   = self._bg
        ret._mod  = self._mod
        ret._clean = self._clean
        if modifier and self._colorMod:
            ret._colorMod = self._colorMod.copy()
        return ret

class _TTkColorModifier():
    def __init__(self, *args, **kwargs): pass
    def setParam(self, *args, **kwargs): pass
    def copy(self): return self

class TTkColorGradient(_TTkColorModifier):
    __slots__ = ('_increment', '_val', '_buffer')
    _increment: int; _val: int
    def __init__(self, *args, **kwargs):
        _TTkColorModifier.__init__(self, *args, **kwargs)
        self._increment = kwargs.get("increment",0)
        self._val = 0
        self._buffer = {}
    def setParam(self, *args, **kwargs):
        self._val = kwargs.get("val",0)
    def exec(self, x, y, color):
        def _applyGradient(c):
            if not c: return c
            multiplier = abs(self._val + y)
            r = int(c[0])+ self._increment * multiplier
            g = int(c[1])+ self._increment * multiplier
            b = int(c[2])+ self._increment * multiplier
            r = max(min(255,r),0)
            g = max(min(255,g),0)
            b = max(min(255,b),0)
            return (r,g,b)

        bname = str(color)
        # I made a buffer to keep all the gradient values to speed up the paint process
        if bname not in self._buffer:
            self._buffer[bname] = [None]*(256*2)
        id = self._val + y - 256
        if self._buffer[bname][id] is not None:
            return self._buffer[bname][id]
        copy = color.copy(modifier=False)
        copy._fg = _applyGradient(color._fg)
        copy._bg = _applyGradient(color._bg)
        self._buffer[bname][id] = copy
        return self._buffer[bname][id]

    def copy(self):
        return self

class TTkColor(_TTkColor):
    ''' TermTk Color helper

    .. role:: strike
        :class: strike

    .. role:: underline
        :class: underline

    The TTkColor constructor creates the color based on HEX values.

    Example:

    .. code:: python

        # Foreground only colors:
        color_fg_red   = TTkColor.fg('#FF0000')
        color_fg_green = TTkColor.fg('#00FF00')
        color_fg_blue  = TTkColor.fg('#0000FF')

        # Background only colors:
        color_bg_red   = TTkColor.bg('#FF0000')
        color_bg_green = TTkColor.bg('#00FF00')
        color_bg_blue  = TTkColor.bg('#0000FF')

        # Combine
        color_1 = color_fg_red + color_bg_blue
        color_2 = color_fg_red + TTkColor.bg('#FFFF00')
        color_3 = color_2 + TTkColor.UNDERLINE + TTkColor.BOLD
    '''
    RST = _TTkColor()
    '''Reset to the default terminal color and modifiers'''

    # Modifiers:
    BOLD         = _TTkColor(mod=TTkHelper.Color.BOLD)
    '''**Bold** modifier'''
    ITALIC       = _TTkColor(mod=TTkHelper.Color.ITALIC)
    '''*Italic* modifier'''
    UNDERLINE    = _TTkColor(mod=TTkHelper.Color.UNDERLINE)
    ''':underline:`Underline` modifier'''
    STRIKETROUGH = _TTkColor(mod=TTkHelper.Color.STRIKETROUGH)
    ''':strike:`Striketrough` modifier'''

    BLINKING     = _TTkColor(mod=TTkHelper.Color.BLINKING)
    '''"Blinking" modifier'''

    @staticmethod
    def hexToRGB(val):
        r = int(val[1:3],base=16)
        g = int(val[3:5],base=16)
        b = int(val[5:7],base=16)
        return (r,g,b)

    @staticmethod
    def ansi(ansi):
        fg,bg,mod,clean = TTkHelper.Color.ansi2rgb(ansi)
        return TTkColor(fg=fg, bg=bg, mod=mod, clean=clean)

    @staticmethod
    def fg(*args, **kwargs):
        ''' Helper to generate a Foreground color

        Example:

        .. code:: python

            color_1 = TTkColor.fg('#FF0000')
            color_2 = TTkColor.fg(color='#00FF00')
            color_3 = TTkColor.fg('#0000FF', modifier=TTkColorGradient(increment=6))

        :param str color: the color representation in (str)HEX
        :type color: str
        :param str modifier: (experimental) the color modifier to be used to improve the **kinkiness**
        :type modifier: TTkColorModifier, optional
        '''
        mod = kwargs.get('modifier', None )
        if len(args) > 0:
            color = args[0]
        else:
            color = kwargs.get('color', "" )
        return TTkColor(fg=TTkColor.hexToRGB(color), colorMod=mod)

    @staticmethod
    def bg(*args, **kwargs):
        ''' Helper to generate a Background color

        Example:

        .. code:: python

            color_1 = TTkColor.bg('#FF0000')
            color_2 = TTkColor.bg(color='#00FF00')
            color_3 = TTkColor.bg('#0000FF', modifier=TTkColorGradient(increment=6))

        :param str color: the color representation in (str)HEX
        :type color: str
        :param str modifier: (experimental) the color modifier to be used to improve the **kinkiness**
        :type modifier: TTkColorModifier, optional
        '''
        mod = kwargs.get('modifier', None )
        if len(args) > 0:
            color = args[0]
        else:
            color = kwargs.get('color', "" )
        return TTkColor(bg=TTkColor.hexToRGB(color), colorMod=mod)
