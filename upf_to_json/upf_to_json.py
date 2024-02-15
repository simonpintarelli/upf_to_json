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

    try:
        cutoff_index = pp_dict['pseudo_potential']['header']['cutoff_radius_index']
        click.echo('cutoff: {:.3f} a.u.'.format(pp_dict['pseudo_potential']['radial_grid'][cutoff_index]))
    except KeyError:
        # cutoff_radius_index not in header
        pass
    # lmax

    paw_lmax = 0
    if 'paw_data' in pp_dict['pseudo_potential']:
        paw_data = pp_dict['pseudo_potential']['paw_data']
        paw_lmax  = max([wfc['angular_momentum'] for wfc in paw_data['ae_wfc']] +
                        [wfc['angular_momentum'] for wfc in paw_data['ps_wfc']])


    aug_lmax = max([aug['angular_momentum'] for aug in pp_dict['pseudo_potential']['augmentation']])
    try:
        print([x['label'] for x in pp_dict['pseudo_potential']['beta_projectors']])
    except KeyError:
        print('beta projectors aren\'t labelled')

    print('\n')
    print(f'lmax (aug)            : {aug_lmax}')
    if 'paw_data' in pp_dict['pseudo_potential']:
        print(f'lmax (paw)            : {paw_lmax}')
    print('lmax (beta-projectors): {}'.format(max([x['angular_momentum'] for x in pp_dict['pseudo_potential']['beta_projectors']])))
