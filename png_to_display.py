#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# png_to_bmp.py - send a PNG to the Waveshare 10.3 inch display.
# It is assumed the PNG is already in grayscale (of whatever bit depth) and the right size.
# Garrett Birkel
# Version 0.1
#
# LICENSE
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the author be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#
# Copyright (c) 2025 Garrett Birkel

import argparse, os, re, sys
import subprocess
from PNG_to_BMP.png_to_bmp import png_to_bmp


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Send a PNG to the Waveshare display")
    args.add_argument("--quiet", "-q", action='store_false', dest='verbose',
                      help="reduce log output")
    args.add_argument('--in', type=argparse.FileType('rb'), default=sys.stdin, dest='input_file',
                      help='Input PNG file', required=True)
    args = args.parse_args()

    png_to_bmp(
        verbose=args.verbose,
        input_file=args.input_file,
        output_file="to_display.bmp"
    )

    display_command = "./IT8951_Utility/it8951utility -1.23 1 to_display.bmp"
    output = subprocess.check_output(display_command, shell=True)
    if args.verbose:
        print(output)
