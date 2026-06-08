"""Project configuration: dataset selection and analysis constants.

Responsibility
--------------
Centralize the reproducible configuration for the version 1 analysis slice so
that subjects, runs, paths, and event-mapping conventions live in one place
rather than being scattered across notebooks.

Intended contents (to be implemented in a later stage):

- The version 1 subject selection (subjects 1, 2, 3).
- The version 1 run selection (runs 1, 2, 4, 8, 12).
- A run-type classification (baseline vs motor-imagery left/right hand).
- The local, git-ignored data directory (``data/raw/``).
- Default epoch window and frequency-band definitions used for reporting.

Important convention
--------------------
Event labels T1/T2 are NOT globally fixed. Their meaning depends on the run
type (see ``docs/dataset_notes.md``). Any event mapping defined here must be
keyed by run number, never by raw event code alone.

Status
------
Version 0.1 scaffolding. The module exposes its planned constants below as
references for documentation and tests; richer configuration objects are
deferred to a later stage.
"""

from __future__ import annotations

# Version 1 analysis slice (see docs/project_brief.md and docs/dataset_notes.md).
# These literals document the intended scope. They are intentionally simple so
# the placeholder tests can assert the scope without importing heavy deps.
SUBJECTS: tuple[int, ...] = (1, 2, 3)
RUNS: tuple[int, ...] = (1, 2, 4, 8, 12)

# Local directory where downloaded raw EDF files will live. This path is
# git-ignored and never committed.
RAW_DATA_DIR: str = "data/raw"


def get_dataset_config() -> dict:
    """Return the resolved dataset configuration for the v1 slice.

    Planned (not yet implemented in v0.1).
    """
    raise NotImplementedError(
        "eeg_lab.config.get_dataset_config is a scaffolding stub."
    )
