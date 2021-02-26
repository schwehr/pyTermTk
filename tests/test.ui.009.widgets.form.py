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

import sys, os
import random

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

ttk.TTkLog.use_default_file_logging()

root = ttk.TTk()
win_form1 = ttk.TTkWindow(parent=root,pos=(1,1), size=(60,30), title="Test Window 1", border=True)
win_form1.setLayout(ttk.TTkGridLayout(columnMinWidth=1))

win_form1.layout().addWidget(ttk.TTkButton(text='Button 1'),0,0)
win_form1.layout().addWidget(ttk.TTkButton(text='Button 2'),1,0)

win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Test 1'),2,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='Line Edit Test 1'),2,2)
win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Test 2'),3,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='Line Edit Test 2'),3,2)
win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Test 3'),4,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='Line Edit Test 3'),4,2)
win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Test 4'),5,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='Line Edit Test 4'),5,2)
win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Test 5'),6,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='Line Edit Test 5'),6,2)

win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Input Number'),7,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='123456', inputType=ttk.TTkK.Input_Number),7,2)
win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Input Wrong Number'),8,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='No num Text', inputType=ttk.TTkK.Input_Number),8,2)

win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Input Password'),9,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='Password', inputType=ttk.TTkK.Input_Password),9,2)
win_form1.layout().addWidget(ttk.TTkLabel(text='Line Edit Number Password'),10,0)
win_form1.layout().addWidget(ttk.TTkLineEdit(text='Password', inputType=ttk.TTkK.Input_Password+ttk.TTkK.Input_Number),10,2)

win_form1.layout().addWidget(ttk.TTkSpacer(),11,0)


root.mainloop()