#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 05.02.2018

@author: DLF
'''
from os.path import expanduser
from datetime import datetime
from pathlib import Path
from shutil import move
import argparse
import logging
import json
import glob
import sys
import os
from tatorterp import Episode, Matcher
from tatorterp.grabber import WikipdediaDEGrabber

logger = logging.getLogger("tatorter")
logging.basicConfig()
logger.setLevel(logging.INFO)

file_rename_pattern = "{episode_index:0>4}--{location}--{title}"

if __name__ == "__main__":
    home = expanduser("~")
    default_cache_path = "{}/.tatorter.cache".format(home)
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-c","--cache",
        help="file for caching episode data (default: {})".format(default_cache_path),
        default=default_cache_path
        )
    argparser.add_argument(
        "files",
        nargs=1
        )
    
    args = argparser.parse_args()
    
    cache_days = 1
    cache_path = Path(args.cache)
    
    cache_used = False
    episodes = None
    
    if cache_path.is_file():
        last_modified_date = datetime.fromtimestamp(os.path.getmtime(cache_path))
        now = datetime.now()
        if (now - last_modified_date).days < cache_days:
            cache_used = True
            logging.info("Loading cache...")
            with open(cache_path,mode="r",encoding="utf-8") as cache_file:
                cache = json.load(cache_file)
                episodes = []
                for e in cache:
                    episodes.append(Episode(**e))
        else:
            logger.info("Cache out-dated. ({} days)".format((now - last_modified_date).days))
    else:
        logger.info("No cache file.")
    if not cache_used:
        logging.info("Fetching online data...")
        episodes = WikipdediaDEGrabber().episodes
        logger.info("Storing cache...")
        with open(cache_path,mode="w",encoding="utf-8") as cache_file:
            json.dump([episode.as_dict for episode in episodes], cache_file)
    
    assert len(args.files) == 1
    
    files = glob.glob(args.files[0])
    options_count = 5
    for file in files:
        matcher = Matcher(file, episodes)
        source_file = os.path.basename(file)
        target_path = os.path.dirname(file)
        target_extension = os.path.splitext(file)[1]
        target_names = []
        print ("="*80)
        print ("Choose new file name for file {}".format(source_file)) 
        for ix in range(options_count):
            match = matcher.match_list[ix]
            target_name = file_rename_pattern.format(**(match[1].as_dict)) + target_extension
            target_names.append(target_name)
            print ("–"*80 + "\n" + "{ix:>5} {match:>6}| {target_name}".format(
                ix=ix+1,
                match="({}%)".format(match[0]),
                target_name = target_name
                ))
        selection = None
        while selection is None:
            print ("–"*80)
            selection_text = input("Choose a new file name ([1..{max}]), skip this file (s) or cancel this script (q):".format(max=options_count))
            if selection_text in [str(i+1) for i in range(options_count)]:
                selection = int(selection_text)
            if selection_text in ['s', 'q']:
                selection = selection_text
        if selection == 's':
            continue
        if selection == 'q':
            sys.exit(0)
        full_target_name = os.path.join(target_path, target_names[selection-1])
        if Path(full_target_name).is_file():
            selection_text = input("Target file {} exists! Overwrite? (y/n)".format(full_target_name))
            while selection_text.lower() not in ['y','n']:
                selection_text = input("I just understand 'y' or 'n'. Overwrite? (y/n)".format(full_target_name))
            if selection_text == 'n':
                continue
        try:
            move(file, full_target_name)
            print ("Moved to {}".format(full_target_name))
        except IOError as e:
            print("File could not be copied ({0}): {1}".format(e.errno, e.strerror))   
                
                                       
        
        
            
            
            
            
            