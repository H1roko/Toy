"""
module存放需要引入的包
并初始化pygame音乐模块
"""

import os
# 隐藏pygame提示
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
import sys
import time
import random
import datetime
from time import sleep
from email import message
from turtle import update
from secrets import choice
from datetime import datetime
from rich import box
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.table import Column
from rich.layout import Layout
from rich.console import Console, Group
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.live import Live