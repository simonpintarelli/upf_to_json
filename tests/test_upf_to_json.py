import pytest

from upf_to_json import upf_to_json
from deepdiff import DeepDiff
import gzip, json


def diff(fname, ref_json_gz):
    with open(fname, "r") as fh:
        dd = upf_to_json(fh.read(), fname=fname)
    with gzip.open(ref_json_gz, "rt") as fh:
        dd_ref = json.load(fh)
    diff = DeepDiff(dd, dd_ref)
    assert diff == {}


def test_gbrv15():
    fname = "cr_pbe_v1.5.uspp.F.UPF"
    diff(fname, fname + ".json.gz")


def test_gbrv14():
    fname = "cl_pbe_v1.4.uspp.F.UPF"
    diff(fname, fname + ".json.gz")


def test_sg15():
    fname = "Kr_ONCV_PBE-1.0.oncvpsp.upf"
    diff(fname, fname + ".json.gz")


def test_pseudo_dojo():
    fname = "Hf-sp.oncvpsp.upf"
    diff(fname, fname + ".json.gz")


def test_atompaw():
    fname = "Gd.GGA-PBE-paw-v1.0.UPF"
    diff(fname, fname + ".json.gz")


def test_pslibrary_paw():
    fname = "Al.pbe-n-kjpaw_psl.1.0.0.UPF"
    diff(fname, fname + ".json.gz")


def test_pslibrary_new():
    fname = "Ac.us.z_11.ld1.psl.v1.0.0-high.upf"
    diff(fname, fname + ".json.gz")
