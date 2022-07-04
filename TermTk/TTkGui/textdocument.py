#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.string import TTkString

class TTkTextDocument():
    __slots__ = (
        '_dataLines',
        # Signals
        'contentsChange', 'contentsChanged',
        )
    def __init__(self, *args, **kwargs):
        self.contentsChange = pyTTkSignal(int,int,int,int) # int,int position, int charsRemoved, int charsAdded
        self.contentsChanged = pyTTkSignal()
        text =  kwargs.get('text',"")
        self._dataLines = [TTkString(t) for t in text.split('\n')]

    def lineCount(self):
        return len(self._dataLines)

    def characterCount(self):
        return sum([len[x] for x in self._dataLines])+self.lineCount()

    def setText(self, text):
        self._dataLines = [TTkString(t) for t in text.split('\n')]
        self.contentsChanged.emit()
        self.contentsChange.emit(0,0,0,len(text))

    def appendText(self, text):
        if type(text) == str:
            text = TTkString() + text
        oldLines = len(self._dataLines)
        oldPos = len(self._dataLines[-1])
        self._dataLines += text.split('\n')
        self.contentsChanged.emit()
        self.contentsChange.emit(oldLines,oldPos,0,len(text))


