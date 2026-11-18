# UPF to JSON converter

UPF is a file format to describe atomic pseudo-potentials used by (DFT) density
functional theory codes. This package provides scripts for converting UPF v1 and
UPF v2 (Unified Pseudopotential Format) to json format as required by the SIRIUS
DFT library [SIRIUS github](https://github.com/electronic-structure/SIRIUS).


More information about the unified pseudopotential format can be found here:
https://www.quantum-espresso.org/pseudopotentials/unified-pseudopotential-format


## Installation

From PyPI:

```sh
# as a standalone CLI tool
uv tool install upf_to_json
# or run it once without installing
uvx --from upf_to_json upf2json --help
# or as a library in a uv project / with pip
uv add upf_to_json
pip install upf_to_json
```

From a local checkout:

```sh
uv tool install .
```

## CLI interface

The package installs the `upf2json` command:

```
Usage: upf2json [OPTIONS] COMMAND [ARGS]...

  Convert UPF v1/v2 pseudopotentials to SIRIUS JSON.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  convert  Convert UPF file INFILE to JSON (OUTFILE, default: stdout).
  summary  Print header, cutoff radius and lmax info of INFILE.
```

### Examples

```sh
# convert, writing to a file (omit OUTFILE to write to stdout)
upf2json convert Al.pbe-n-kjpaw_psl.1.0.0.UPF Al.json

# inspect a pseudopotential: header fields, cutoff radius, lmax
upf2json summary Al.pbe-n-kjpaw_psl.1.0.0.UPF

upf2json --version
```

Warnings about inconsistent UPF metadata are printed to stderr.

## Python API

```python
from upf_to_json import upf_to_json

with open("Al.pbe-n-kjpaw_psl.1.0.0.UPF") as fh:
    pp_dict = upf_to_json(fh.read(), fname="Al.pbe-n-kjpaw_psl.1.0.0.UPF")
```
