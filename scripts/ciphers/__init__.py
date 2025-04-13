import importlib
import pkgutil
import os
import base64
import base58

# Make base64 available in the package namespace
__all__ = ["base64"]

package_dir = os.path.dirname(__file__)
# Iterate over all Python files in the directory
for _, module_name, _ in pkgutil.iter_modules([package_dir]):
    if not module_name.startswith("_"):  # Exclude special modules
        module = importlib.import_module(f".{module_name}", package=__name__)
        globals()[module_name] = module  