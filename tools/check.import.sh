#!/bin/sh

__check(){
    grep -r -e "^import" -e "^from" TermTk |
        grep -v -e "from TermTk" -e "import TermTk" |
        grep -v "__init__.py:from \.[^ ]* *import" |
        grep -v -e "import re" -e "import os" -e "import datetime" |
        grep -v \
            -e "from dataclasses" \
            -e "colors.py:from .colors_ansi_map" \
            -e "timer.py:import threading, time" \
            -e "log.py:import inspect" \
            -e "log.py:import logging" \
            -e "log.py:from collections.abc import Callable, Set" \
            -e "from time" -e "input.py:import platform" \
            -e "readinputlinux.py:import sys, os, select" \
            -e "readinputlinux_thread.py:import sys, os, select" \
            -e "readinputlinux_thread.py:import threading" \
            -e "readinputlinux_thread.py:import queue" \
            -e "term.py:import sys, os, signal" \
            -e "ttk.py:import signal" \
            -e "ttk.py:import time" \
            -e "ttk.py:import queue" \
            -e "filebuffer.py:import threading"
} ;

if __check ;  then
    echo "Failed Dependencies verification!!!" ;
    echo "Please check:" ;
    echo "#######################"
    __check ;
    echo "#######################"
    exit 1 ;
else
    echo "Dependencies Verified!!!"
    exit 0 ;
fi ;
