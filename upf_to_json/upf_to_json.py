# -*- coding: utf-8 -*-
"""UPF to json converter"""

from __future__ import absolute_import
from .upf1_to_json import parse_upf1_from_string
from .upf2_to_json import parse_upf2_from_string


def get_upf_version(upf):
    """Get UPF version."""
    line = upf.split('\n')[0]
    if '<PP_INFO>' in line:
        return 1
    if 'UPF version' in line:
        return 2
    return 0


def upf_to_json(upf_str, fname):
    """Convert UPF to python dictionary.

    :param upf_str: upf as string
    :param fname: filename of the original .UPF file
    """
    version = get_upf_version(upf_str)
    if version == 0:
        return None
    if version == 1:
        pp_dict = parse_upf1_from_string(upf_str)
    if version == 2:
        pp_dict = parse_upf2_from_string(upf_str)

    pp_dict['pseudo_potential']['header']['original_upf_file'] = fname
    return pp_dict
