import os
import sys
import pytest


def test_import():
    """Test that certum_signer module can be imported"""
    try:
        import src.certum_signer
        assert True
    except ModuleNotFoundError as e:
        # tkinter is not available on Linux CI, which is expected
        if "tkinter" in str(e):
            pytest.skip("tkinter not available (Windows GUI app)")
        else:
            raise


def test_certum_signer_module_exists():
    """Test that the certum_signer.py file exists in src/"""
    src_path = os.path.join(os.path.dirname(__file__), "..", "src", "certum_signer.py")
    assert os.path.exists(src_path), "certum_signer.py should exist in src/"
