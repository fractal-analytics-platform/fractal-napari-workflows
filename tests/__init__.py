import json
from pathlib import Path

import fractal_napari_workflows

PACKAGE_DIR = Path(fractal_napari_workflows.__file__).parent
MANIFEST_FILE = PACKAGE_DIR / "__FRACTAL_MANIFEST__.json"
with MANIFEST_FILE.open("r") as f:
    MANIFEST = json.load(f)
