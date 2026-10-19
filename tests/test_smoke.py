import importlib

import pytest

MODULES = ["ingest", "bronze", "silver", "gold", "quality"]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    importlib.import_module(f"crete_rentals.{name}")
