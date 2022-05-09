import pytest

from upf_to_json import upf_to_json

def call_upf2json(fname):
    """Check that upf_to_json doesn't throw an exception."""
    try:
        with open(fname, 'r') as fh:
            dd = upf_to_json(fh.read(), fname=fname)
    except:
        pytest.fail('failed to convert: ', fname)

def test_gbrv15():
    fname = 'cr_pbe_v1.5.uspp.F.UPF'
    call_upf2json(fname)

def test_gbrv14():
    fname = 'cl_pbe_v1.4.uspp.F.UPF'
    call_upf2json(fname)

def test_sg15():
    fname = 'Kr_ONCV_PBE-1.0.oncvpsp.upf'
    call_upf2json(fname)

def test_pseudo_dojo():
    fname = 'Hf-sp.oncvpsp.upf'
    call_upf2json(fname)

def test_atompaw():
    fname = 'Gd.GGA-PBE-paw-v1.0.UPF'
    call_upf2json(fname)

def test_pslibrary_paw():
    fname = 'Al.pbe-n-kjpaw_psl.1.0.0.UPF'
    call_upf2json(fname)
