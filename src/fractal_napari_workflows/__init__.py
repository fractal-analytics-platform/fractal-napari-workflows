"""Package description."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("fractal_napari_workflows")
except PackageNotFoundError:
    __version__ = "uninstalled"
