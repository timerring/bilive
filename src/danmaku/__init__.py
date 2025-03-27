# Copyright (c) 2024 bilive.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .DanmakuConvert.dmconvert import convert_xml_to_ass

__all__ = ['convert_xml_to_ass']