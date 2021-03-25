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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkListWidgetText(TTkLabel):
    __slots__ = ('clicked', '_selected', '_highlighted')
    def __init__(self, *args, **kwargs):
        TTkLabel.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkListWidgetText' )
        # Define Signals
        self.clicked = pyTTkSignal(_TTkListWidgetText)
        self._selected = False
        self._highlighted = False

    def _updateColor(self):
        if self._highlighted:
            if self._selected:
                self.color = TTkCfg.theme.listColorHighlighted + TTkColor.UNDERLINE
            else:
                self.color = TTkCfg.theme.listColorHighlighted
        elif self._selected:
            self.color = TTkCfg.theme.listColorSelected
        else:
            self.color = TTkCfg.theme.listColor

    def mouseReleaseEvent(self, evt):
        self.clicked.emit(self)
        return True

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, selected):
        if self._selected != selected:
            self._selected = selected
            self._updateColor()

    @property
    def highlighted(self):
        return self._highlighted

    @highlighted.setter
    def highlighted(self, highlighted):
        if self._highlighted != highlighted:
            self._highlighted = highlighted
            self._updateColor()


class TTkListWidget(TTkAbstractScrollView):
    __slots__ = ('itemClicked', 'textClicked', '_color', '_selectedColor', '_selectedItems', '_selectionMode', '_highlighted', '_items')
    def __init__(self, *args, **kwargs):
        # Default Class Specific Values
        self._selectionMode = kwargs.get("selectionMode", TTkK.SingleSelection)
        self._selectedItems = []
        self._items = []
        self._highlighted = None
        self._color = TTkCfg.theme.listColor
        self._selectedColor = TTkCfg.theme.listColorSelected
        # Signals
        self.itemClicked = pyTTkSignal(TTkWidget)
        self.textClicked = pyTTkSignal(str)
        # Init Super
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkListWidget' )
        self.viewChanged.connect(self._viewChangedHandler)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().groupMoveTo(-x,-y)

    @pyTTkSlot(_TTkListWidgetText)
    def _labelSelectedHandler(self, label):
        if self._selectionMode == TTkK.SingleSelection:
            for i in self._selectedItems:
                i.selected = False
                i.color = TTkCfg.theme.listColor
            label.selected = True
        elif self._selectionMode == TTkK.MultiSelection:
            label.selected = not label.selected
        if label.selected:
            self._selectedItems.append(label)
        else:
            self._selectedItems.remove(label)
        self._highlighted = label
        self.setFocus()
        self.textClicked.emit(label.text)

    def setSelectionMode(self, mode):
        self._selectionMode = mode

    def selectedLabels(self):
        return [i.text for i in self._selectedItems]

    def resizeEvent(self, w, h):
        maxw = 0
        for item in self.layout().children():
            maxw = max(maxw,item.minimumWidth())
        maxw = max(self.width(),maxw)
        for item in self.layout().children():
            x,y,_,h = item.geometry()
            item.setGeometry(x,y,maxw,h)
        self.viewChanged.emit()

    def viewFullAreaSize(self) -> (int, int):
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w , h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def addItem(self, item):
        if isinstance(item, str):
            label = _TTkListWidgetText(text=item, width=max(len(item),self.width()))
            label.clicked.connect(self._labelSelectedHandler)
            return self.addItem(label)
        self._items.append(item)
        _,y,_,h = self.layout().fullWidgetAreaGeometry()
        self.addWidget(item)
        item.move(0,y+h)
        _,_,fw,_ = self.layout().fullWidgetAreaGeometry()
        w = self.width()
        for item in self.layout().children():
            x,y,_,h = item.geometry()
            item.setGeometry(x,y,max(w-1,fw),h)
        self.viewChanged.emit()

    def _moveToHighlighted(self):
        index = self._items.index(self._highlighted)
        h = self.height()
        offx,offy = self.getViewOffsets()
        if index >= h+offy-1:
            TTkLog.debug(f"{index} {h} {offy}")
            self.viewMoveTo(offx, index-h+1)
        elif index <= offy:
            self.viewMoveTo(offx, index)

    def keyEvent(self, evt):
        if not self._highlighted: return
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            if self._highlighted:
               self._highlighted.clicked.emit(self._highlighted)
            return True
        elif evt.type == TTkK.SpecialKey:
            if evt.key == TTkK.Key_Tab:
                return False
            index = self._items.index(self._highlighted)
            offx,offy = self.getViewOffsets()
            if evt.key == TTkK.Key_Up:
                index = max(0, index-1)
            elif evt.key == TTkK.Key_Down:
                index = min(len(self._items)-1, index+1)
            elif evt.key == TTkK.Key_PageUp:
                index = 0
            elif evt.key == TTkK.Key_PageDown:
                index = len(self._items)-1
            elif evt.key == TTkK.Key_Right:
                self.viewMoveTo(offx+1, offy)
            elif evt.key == TTkK.Key_Left:
                self.viewMoveTo(offx-1, offy)
            elif evt.key == TTkK.Key_Home:
                self.viewMoveTo(0, offy)
            elif evt.key == TTkK.Key_End:
                self.viewMoveTo(0x10000, offy)

            self._highlighted.highlighted = False
            self._highlighted = self._items[index]
            self._highlighted.highlighted = True
            self._moveToHighlighted()
            return True
        return False

    def focusInEvent(self):
        if not self._items: return
        if not self._highlighted:
            self._highlighted = self._items[0]
        self._highlighted.highlighted=True
        self._moveToHighlighted()

    def focusOutEvent(self):
        if self._highlighted:
            self._highlighted.highlighted=False