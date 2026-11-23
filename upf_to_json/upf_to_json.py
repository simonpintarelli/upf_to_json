from .upf1_to_json import parse_upf1_from_string
from .upf2_to_json import (
    parse_upf2_from_string,
    add_paw_core_kinetic_density,
    add_kinetic_augmentation,
)
import json
import click


def get_upf_version(upf):
    lines = upf.split("\n")
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
        raise Exception("Unkown UPF version")

    pp_dict["pseudo_potential"]["header"]["original_upf_file"] = fname
    return pp_dict


@click.group()
@click.version_option(package_name="upf_to_json")
def cli():
    """Convert UPF v1/v2 pseudopotentials to SIRIUS JSON."""


@cli.command()
@click.argument("infile", type=click.File(mode="rb"))
@click.argument("outfile", type=click.File(mode="w"), default="-")
@click.option(
    "--paw-core-xml",
    type=click.Path(exists=True, dir_okay=False),
    help="Matching ATOMPAW XML with AE and pseudo core kinetic densities.",
)
@click.option(
    "--kinetic-augmentation-json",
    type=click.Path(exists=True, dir_okay=False),
    help="Generator-supplied ultrasoft r^2 T_ij^L tables matched by the UPF SHA-256.",
)
def convert(infile, outfile, paw_core_xml, kinetic_augmentation_json):
    """Convert UPF file INFILE to JSON (OUTFILE, default: stdout)."""
    # keep the raw text (original line endings) for the SHA-256 check
    upf_raw = infile.read().decode("utf-8")
    upf_str = upf_raw.replace("\r\n", "\n").replace("\r", "\n")
    pp_dict = upf_to_json(upf_str, fname=infile.name)
    if paw_core_xml:
        try:
            add_paw_core_kinetic_density(pp_dict, paw_core_xml)
        except (ValueError, RuntimeError, OSError) as error:
            raise click.BadParameter(str(error), param_hint="--paw-core-xml")
    if kinetic_augmentation_json:
        try:
            add_kinetic_augmentation(pp_dict, upf_raw, kinetic_augmentation_json)
        except (ValueError, RuntimeError, OSError) as error:
            raise click.BadParameter(
                str(error), param_hint="--kinetic-augmentation-json"
            )
    outfile.write(json.dumps(pp_dict))


@cli.command()
@click.argument("infile", type=click.File(mode="r"))
def summary(infile):
    """Print header, cutoff radius and lmax info of INFILE."""
    pp_dict = upf_to_json(infile.read(), fname=infile.name)
    click.echo(json.dumps(pp_dict["pseudo_potential"]["header"], indent=2))

    try:
        cutoff_index = pp_dict["pseudo_potential"]["header"]["cutoff_radius_index"]
        click.echo(
            "cutoff: {:.3f} a.u.".format(
                pp_dict["pseudo_potential"]["radial_grid"][cutoff_index]
            )
        )
    except KeyError:
        # cutoff_radius_index not in header
        pass
    # lmax

    paw_lmax = 0
    if "paw_data" in pp_dict["pseudo_potential"]:
        paw_data = pp_dict["pseudo_potential"]["paw_data"]
        paw_lmax = max(
            [wfc["angular_momentum"] for wfc in paw_data["ae_wfc"]]
            + [wfc["angular_momentum"] for wfc in paw_data["ps_wfc"]]
        )

    aug_lmax = max(
        [aug["angular_momentum"] for aug in pp_dict["pseudo_potential"]["augmentation"]]
    )
    try:
        print([x["label"] for x in pp_dict["pseudo_potential"]["beta_projectors"]])
    except KeyError:
        print("beta projectors aren't labelled")

    print("\n")
    print(f"lmax (aug)            : {aug_lmax}")
    if "paw_data" in pp_dict["pseudo_potential"]:
        print(f"lmax (paw)            : {paw_lmax}")
    print(
        "lmax (beta-projectors): {}".format(
            max(
                [
                    x["angular_momentum"]
                    for x in pp_dict["pseudo_potential"]["beta_projectors"]
                ]
            )
        )
    )
