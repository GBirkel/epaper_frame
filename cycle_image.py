#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# cycle_image.py - choose an image from the library and send it to the display.
# It is assumed the image is already in grayscale (of whatever bit depth) and the right size.
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
from png_to_display import png_to_display
from datetime import *
from common_utils import *
from image_database import *


def cycle_image(verbose=False, specific_id=None):

    config = read_config()
    if config is None:
        print('Error reading your config.xml file!')
        sys.exit(2)

    conn = None
    cur = None

    # create a database connection
    conn = connect_to_local_db(config['database'], verbose)
    if not conn:
        print("Database could not be opened")
        os._exit(os.EX_IOERR)
    create_tables_if_missing(conn, verbose)
    cur = conn.cursor()

    status = get_status_or_defaults(cur, None, None)

    images = get_all_images(cur, verbose)
    if verbose:
        print("%s images in library." % (len(images)))
        if status['last_display'] is not None:
            last_display_datetime = datetime.utcfromtimestamp(status['last_display'])
            print("Last run at %s." % (pretty_datetime(last_display_datetime)))

    chosen_image = images[2]
    if verbose:
        print("Chose image %s/%s." % (chosen_image['group_name'], chosen_image['filename']))
        if chosen_image['last_display'] is None:
            print("First time displaying this image.")
        else:
            last_display_datetime = datetime.utcfromtimestamp(chosen_image['last_display'])
            print("Display count %s, last displayed %s." % (chosen_image['display_count'], last_display_datetime))
        
    image_path = os.path.join(config['library'], chosen_image['group_name'], chosen_image['filename'])
    png_to_display(verbose, image_path)
    report_image_as_displayed(cur, verbose, chosen_image['id'])

    current_date = calendar.timegm(datetime.utcnow().utctimetuple())
    status['last_display'] = current_date
    set_status(cur, status)

    finish_with_database(conn, cur)


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Choose an image from the library and display it")
    args.add_argument("--quiet", "-q", action='store_false', dest='verbose',
                      help="reduce log output")
    args.add_argument('--id', type=str, default=None, dest='specific_id',
                      help='Specific image ID to display', required=False)
    args = args.parse_args()

    cycle_image(
        verbose=args.verbose,
        specific_id=args.specific_id,
    )
