#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import re
from collections import Counter
import click

CONTAINER = r'(?P<pattern>{})'
ARG_PATTERN = CONTAINER.format('\{\{(?P<arg>.*?)\}\}')
IN_EX_PATTERN = r'{}|(.)'.format(ARG_PATTERN)

def count_args(template):
    """
    From given template, find all {{arguments}} inside.
    """
    matches = re.finditer(ARG_PATTERN, template)
    args = [match.groupdict()['arg'] for match in matches]
    return Counter(args)

def split_items(context):
    """
    From given context, split this items seprated by '----'
    """
    return [s.strip('\n') for s in re.split(r'\n----+\n', context)]

def format_items(items):
    """
    Given items, format the specified form for save.
    """
    return '\n----\n'.join(items)

def build_text(template, arg2items):
    """
    Make the output text based on template
    """
    output = []
    for matches in re.findall(IN_EX_PATTERN, template, re.DOTALL):
        if matches[0] != '': # something to replace
            output.append(arg2items[matches[1]].pop(0))
        else:
            output.append(matches[2])
    return ''.join(output)

@click.command()
@click.option('--publish', 
    default=None,
    help='Write the output file and make the changes on input files')
@click.argument('filename')
def main(filename, publish):
    template = open(filename).read()
    count_args = count_args(template)
    args = count_args.keys()
    arg2filename = {arg: arg for arg in args}
    arg2context = {arg: open(fn).read() for arg, fn in arg2filename.items()}
    arg2items = {arg: split_items(c) for arg, c in arg2context.items()}
    results = build_text(template, arg2items) # arg2items was modified
    if publish is not None:
        with open(publish, 'w') as f:
            f.write(results)

        for arg, fn in arg2filename.items():
            with open(fn, 'w') as f:
                f.write(format_items(arg2items[arg])) # write modified items
                
    print(results)

if __name__ == '__main__':
    main()

