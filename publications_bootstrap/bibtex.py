# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.utils import six

# from . import six

# special character mapping
special_chars = (
    (r'\"{a}', 'ä'), (r'{\"a}', 'ä'), (r'\"a', 'ä'), (r'H{a}', 'ä'),
    (r'\"{A}', 'Ä'), (r'{\"A}', 'Ä'), (r'\"A', 'Ä'), (r'H{A}', 'Ä'),
    (r'\"{o}', 'ö'), (r'{\"o}', 'ö'), (r'\"o', 'ö'), (r'H{o}', 'ö'),
    (r'\"{O}', 'Ö'), (r'{\"O}', 'Ö'), (r'\"O', 'Ö'), (r'H{O}', 'Ö'),
    (r'\"{u}', 'ü'), (r'{\"u}', 'ü'), (r'\"u', 'ü'), (r'H{u}', 'ü'),
    (r'\"{U}', 'Ü'), (r'{\"U}', 'Ü'), (r'\"U', 'Ü'), (r'H{U}', 'Ü'),
    (r'{‘a}', 'à'), (r'\‘A', 'À'),
    (r'{‘e}', 'è'), (r'\‘E', 'È'),
    (r'{‘o}', 'ò'), (r'\‘O', 'Ò'),
    (r'{‘u}', 'ù'), (r'\‘U', 'Ù'),
    (r'{’a}', 'á'), (r'\’A', 'Á'),
    (r'{’e}', 'é'), (r'\’E', 'É'),
    (r'{’o}', 'ó'), (r'\’O', 'Ó'),
    (r'{’u}', 'ú'), (r'\’U', 'Ú'),
    (r'\`a', 'à'), (r'\`A', 'À'),
    (r'\`e', 'è'), (r'\`E', 'È'),
    (r'\`u', 'ù'), (r'\`U', 'Ù'),
    (r'\`o', 'ò'), (r'\`O', 'Ò'),
    (r'\^o', 'ô'), (r'\^O', 'Ô'),
    (r'\^a', 'â'), (r'\^A', 'Â'),
    (r'\^e', 'ê'), (r'\^E', 'Ê'),
    (r'\^i', 'î'), (r'\^I', 'Î'),
    (r'\^u', 'û'), (r'\^U', 'Û'),
    (r'\ss', 'ß'),
    (r'\%', '%'),
    (r'\ae', 'æ'), (r'\AE', 'Æ'), (r'\aa', 'å'), (r'\AA', 'Å'), (r'\o', 'ø'), (r'\O', 'Ø'),
    # swedish, danish, norwegian
    (r'\c{c}', 'ç'), (r'\c{C}', 'Ç'),  # french, portuguese, etc
    (r'\~a', 'ã'), (r'\~A', 'Ã'),  # portuguese
    (r'\~o', 'õ'), (r'\~O', 'Õ'),
    (r'{\i}', 'ı'), (r'\.{I}', 'İ'), ('\\u{g}', 'ğ'), ('\\u{G}', 'Ğ'), (r'\c{s}', 'ş'),
    (r'\c{S}', 'Ş'))  # turkish


def parse(string):
    """
    Takes a string in BibTex format and returns a list of BibTex entries, where
    each entry is a dictionary containing the entries' key-value pairs.

    @type  string: string
    @param string: bibliography in BibTex format

    @rtype: list
    @return: a list of dictionaries representing a bibliography
    """

    # bibliography
    bib = []

    # make sure we are dealing with unicode strings
    if not isinstance(string, six.text_type):
        string = string.decode('utf-8')

    # replace special characters
    for key, value in special_chars:
        string = string.replace(key, value)
    string = re.sub(r'\\[cuHvs]{?([a-zA-Z])}?', r'\1', string)

    # split into BibTex entries
    entries = re.findall(
        r'(?u)@(\w+)[ \t]?{[ \t]*([^,\s]*)[ \t]*,?\s*((?:[^=,\s]+\s*\=\s*(?:"[^"]*"|{(?:[^{}]*|{[^{}]*})*}|[^,}]*),?\s*?)+)\s*}',
        string)

    for entry in entries:
        # parse entry
        pairs = re.findall(r'(?u)([^=,\s]+)\s*\=\s*("[^"]*"|{(?:[^{}]*|{[^{}]*})*}|[^,]*)', entry[2])

        # add to bibliography
        bib.append({'type': entry[0].lower(), 'key': entry[1]})

        for key, value in pairs:
            # post-process key and value
            key = key.lower()
            if value and value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            if value and value[0] == '{' and value[-1] == '}':
                value = value[1:-1]
            if key not in ['booktitle', 'title']:
                value = value.replace('}', '').replace('{', '')
            else:
                if value.startswith('{') and value.endswith('}'):
                    value = value[1:]
                    value = value[:-1]
            value = value.strip()
            value = re.sub(r'\s+', ' ', value)

            # store pair in bibliography
            bib[-1][key] = value

    return bib
