from .upf1_to_json import parse_upf1_from_string
from .upf2_to_json import parse_upf2_from_string
import json
import click

def get_upf_version(upf):
    lines = upf.split('\n')
    if "<PP_INFO>" in lines[0]:
        return 1
    elif "UPF version" in lines[0] or "UPF version" in lines[1]:
        return 2
    return 0


def upf_to_json(upf_str, fname):
    """Convert UPF to python dictionary.
    :param upf_str: upf as string
    :param fname: filename of the original .UPF file
    """
    version = get_upf_version(upf_str)
    if version == 1:
        pp_dict = parse_upf1_from_string(upf_str)
    elif version == 2:
        pp_dict = parse_upf2_from_string(upf_str)
    else:
        raise Exception('Unkown UPF version')

    pp_dict['pseudo_potential']['header']['original_upf_file'] = fname
    return pp_dict


@click.group()
def cli():
    pass


@cli.command()
@click.argument('infile', type=click.File(mode='r'))
@click.argument('outfile', type=click.File(mode='w'), default='-')
def convert(infile, outfile):
    pp_dict = upf_to_json(infile.read(), fname=infile.name)
    outfile.write(json.dumps(pp_dict))


@cli.command()
@click.argument('infile', type=click.File(mode='r'))
def summary(infile):
    pp_dict = upf_to_json(infile.read(), fname=infile.name)
    click.echo(json.dumps(pp_dict['pseudo_potential']['header'], indent=2))
