"""Placeholder tests for run-aware event mapping.

The key correctness concern for this dataset is that T1/T2 are interpreted by
run type, not by event code alone (see docs/dataset_notes.md). The real mapping
logic is not implemented in v0.1, so this test is skipped with a note rather
than asserting placeholder behavior.
"""

import pytest


@pytest.mark.skip(reason="Event mapping not implemented in v0.1 (scaffolding).")
def test_t1_t2_depend_on_run_type():
    # Planned: in L/R hand runs (4, 8, 12) T1=left fist, T2=right fist;
    # in hands/feet runs (6, 10, 14) T1=both fists, T2=both feet.
    # T0 is always rest. Mapping must be keyed by run number.
    raise NotImplementedError
