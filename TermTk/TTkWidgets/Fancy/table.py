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
from TermTk.TTkWidgets.Fancy.tableview import TTkFancyTableView
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkFancyTable(TTkAbstractScrollArea):
    __slots__ = (
        '_tableView', 'activated',
        # Forwarded Methods
        'setAlignment', 'setHeader', 'setColumnSize', 'setColumnColors', 'appendItem' )




    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkFancyTable' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._tableView = TTkFancyTableView(*args, **kwargs)
        # Forward the signal
        self.activated = self._tableView.activated

        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._tableView)
        # Forwarded Methods
        self.setAlignment    = self._tableView.setAlignment
        self.setHeader       = self._tableView.setHeader
        self.setColumnSize   = self._tableView.setColumnSize
        self.setColumnColors = self._tableView.setColumnColors
        self.appendItem      = self._tableView.appendItem




