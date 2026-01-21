"""Contains the list of tasks available to fractal."""

from fractal_task_tools.task_models import (
    ParallelTask,
)

AUTHORS = "Joel Luethi"


DOCS_LINK = "https://github.com/fractal-analytics-platform/fractal-napari-workflows"


INPUT_MODELS = [
    ["fractal_napari_workflows", "io_models.py", "NapariWorkflowsInput"],
    ["fractal_napari_workflows", "io_models.py", "NapariWorkflowsOutput"],
]

TASK_LIST = [
    ParallelTask(
        name="Napari Workflows Wrapper",
        executable="napari_workflows_wrapper.py",
        meta={
            "cpus_per_task": 4,
            "mem": 16000,
        },
        category="Measurement",
        tags=["2D", "3D"],
        docs_info="file:docs_info/napari_workflows_wrapper.md",
    ),
]
