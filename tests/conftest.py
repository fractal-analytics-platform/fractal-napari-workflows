# tests/conftest.py

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pooch
import pytest


@pytest.fixture(scope="session")
def testdata_path() -> Path:
    test_dir = Path(__file__).parent
    return test_dir / "data"


ZENODO_HEADERS = {
    "User-Agent": "pooch (https://github.com/fatiando/pooch) "
    "(https://github.com/fractal-analytics-platform/fractal-napari-workflows)",
    "Accept": "*/*",
}

ZENODO_DOWNLOADER = pooch.HTTPDownloader(headers=ZENODO_HEADERS, timeout=120)


@pytest.fixture(scope="session")
def zenodo_zarr(testdata_path: Path) -> list[str]:
    """
    1. Download/unzip two Zarr containers (3D and MIP) from Zenodo, via pooch
    2. Copy the two Zarr containers into tests/data/<DOI_slug>/
    {plate.zarr,plate_mip.zarr}
    """
    DOI = "10.5281/zenodo.13305156"
    DOI_slug = DOI.replace("/", "_").replace(".", "_")

    platenames = ["plate.zarr", "plate_mip.zarr"]
    rootfolder = testdata_path / DOI_slug
    folders = [rootfolder / plate for plate in platenames]

    record_id = "13305156"
    base_url = f"https://zenodo.org/records/{record_id}/files/"
    # If you ever see flaky 403s again, try:
    # base_url = f"https://zenodo.org/records/{record_id}/files/?download=1"
    # Better is to add ?download=1 per file via `urls=` (see below),
    # but keep minimal for now.

    # Pin checksums (no extra requests; integrity checks)
    registry = {
        "20200812-CardiomyocyteDifferentiation14-Cycle1.zarr.zip": (
            "md5:efc21fe8d4ea3abab76226d8c166452c"
        ),
        "20200812-CardiomyocyteDifferentiation14-Cycle1_mip.zarr.zip": (
            "md5:51809479777cafbe9ac0f9fa5636aa95"
        ),
    }

    POOCH = pooch.create(
        path=pooch.os_cache("pooch") / DOI_slug,
        base_url=base_url,
        registry=registry,
        retry_if_failed=10,
        allow_updates=False,
    )

    zarr_names = [
        "20200812-CardiomyocyteDifferentiation14-Cycle1.zarr",
        "20200812-CardiomyocyteDifferentiation14-Cycle1_mip.zarr",
    ]

    for ind, zarr_name in enumerate(zarr_names):
        zip_name = f"{zarr_name}.zip"

        # Download/unzip a single Zarr from Zenodo
        file_paths = POOCH.fetch(
            zip_name,
            downloader=ZENODO_DOWNLOADER,
            processor=pooch.Unzip(extract_dir=zarr_name),
        )

        # Pooch returns a list of extracted paths; derive the folder
        # containing the .zarr
        zarr_full_path = file_paths[0].split(zarr_name)[0] + zarr_name
        folder = folders[ind]

        # Copy the downloaded Zarr into tests/data (replace if existing)
        if os.path.isdir(str(folder)):
            shutil.rmtree(str(folder))
        folder.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(Path(zarr_full_path) / zarr_name, folder)

    return [str(f) for f in folders]
