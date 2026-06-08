# eeg-signal-processing-lab - AI Multitask Execution Guide

## Purpose

This guide is written for an AI multitask or multi-agent system that will implement the project later. It defines the mission, roles, sequence, guardrails, and quality criteria.

No source code is included in this planning package.

## Mission

Build a public GitHub repository that demonstrates practical EEG signal-processing skill using public motor imagery data.

The repository must be reproducible, scientifically cautious, and visually clear.

## Operating Rules

1. Keep version 1 focused on EEG signal processing, not model performance.
2. Use public data only.
3. Do not commit raw dataset files.
4. Cite every external dataset and scientific tool.
5. Document preprocessing decisions before presenting results.
6. Avoid clinical claims.
7. Avoid claiming broad conclusions from a small subject subset.
8. Prefer transparent baseline analysis over complex black-box methods.
9. Keep outputs readable for both software engineers and neurotech reviewers.
10. If a technical decision is uncertain, document the uncertainty and choose the conservative path.

## Agent Roles

### Project Manager Agent

Responsibilities:

- Preserve scope.
- Maintain the backlog.
- Enforce version 1 boundaries.
- Decide when a task is done.
- Prevent drift into classification or deep learning.

Success criteria:

- The final repository tells one clear story.
- No task expands beyond the agreed first release.

### Neurodata Research Agent

Responsibilities:

- Verify dataset facts.
- Confirm citation requirements.
- Map run numbers and event labels.
- Write dataset notes and limitations.

Success criteria:

- Dataset description is accurate.
- T0, T1, and T2 are interpreted with run context.
- References are included and current.

### MNE Implementation Agent

Responsibilities:

- Implement loading, preprocessing, event extraction, epoching, PSD, and report generation when coding begins.
- Use MNE-Python conventions.
- Keep functions small and testable.

Success criteria:

- The notebook/report runs end to end.
- The implementation follows MNE data structures and avoids ad hoc parsing where MNE provides an API.

### Visualization Agent

Responsibilities:

- Produce clear figures.
- Ensure plot labels, units, titles, and legends are readable.
- Prefer plots that explain the pipeline.

Success criteria:

- Figures make the dataset and pipeline understandable without excessive text.
- Plots do not overstate findings.

### Documentation Agent

Responsibilities:

- Write README, docs, captions, references, and limitations.
- Make the project GitHub-profile-ready.
- Translate technical work into a credible public narrative.

Success criteria:

- A visitor can understand the project in under two minutes.
- A technical reader can reproduce the work.

### QA Agent

Responsibilities:

- Check reproducibility.
- Check data leakage into Git.
- Check citation completeness.
- Check event mappings.
- Check visual outputs.
- Check for overclaims.

Success criteria:

- The repository can be shared publicly with confidence.
- The project does not present medical or unsupported conclusions.

## Execution Sequence

### Phase 0 - Scope Lock

Inputs:

- Project brief.
- Technical spec.
- Backlog.

Outputs:

- Confirmed version 1 scope.
- Confirmed subject/run selection.
- Confirmed no-code-to-code transition plan.

Stop conditions:

- If the agent tries to add classification or deep learning, return to scope.

### Phase 1 - Repository Skeleton

Outputs:

- README.
- LICENSE.
- CITATION.
- Docs folder.
- Notebook folder.
- Reports folder.
- Figures folder.
- Source folder if implementation is modular.
- Tests folder if source modules exist.

Quality checks:

- No raw data.
- Clear setup instructions.
- Clear citation section.

### Phase 2 - Dataset Notes

Outputs:

- Dataset facts.
- Run mapping.
- Event mapping.
- License note.
- Citation note.

Quality checks:

- PhysioNet source is linked.
- MNE EEGBCI helper is linked.
- T1/T2 meanings are not treated as universal.

### Phase 3 - First Reproducible Analysis

Outputs:

- Load selected files.
- Inspect raw data.
- Summarize channels, sampling rate, duration, events.
- Generate first figures.

Quality checks:

- Analysis runs from a clean environment.
- Figures are generated from real data.
- The notebook includes interpretation, not only plots.

### Phase 4 - Preprocessing and Epoching

Outputs:

- Conservative preprocessing.
- Epoch creation.
- Before/after notes.
- Event count tables.

Quality checks:

- Preprocessing choices are documented.
- Epoch windows are stated.
- Bad channel handling is explained.

### Phase 5 - Frequency Analysis

Outputs:

- PSD visualizations.
- Baseline comparisons.
- Optional topographic summaries.
- Written interpretation.

Quality checks:

- Frequency bands are defined.
- Units are readable.
- Claims are tied to selected subjects and runs.

### Phase 6 - Publication Polish

Outputs:

- Final README.
- Report.
- Figures.
- Limitations.
- Roadmap.

Quality checks:

- The repo is understandable on GitHub.
- The narrative supports the user's career direction.
- The project looks like a serious neurotech learning artifact.

## Autonomous Decision Boundaries

Agents may decide:

- Exact figure style.
- Whether to use notebook-only or notebook plus HTML report.
- Minor naming conventions.
- Whether to defer ICA if the artifact evidence is not strong.
- Whether to analyze 1, 2, or 3 subjects in version 1 depending on runtime.

Agents must not decide without user approval:

- Change the primary dataset.
- Add deep learning.
- Convert the project into a classifier.
- Add clinical interpretation.
- Add paid tools or private data.
- Publish to GitHub under a different positioning.

## Required Review Checklist

Before finalizing version 1, answer:

- Is the dataset cited?
- Is the license mentioned?
- Are raw files excluded from Git?
- Are subjects and runs stated?
- Are events mapped correctly?
- Are preprocessing decisions documented?
- Are figures generated and readable?
- Are limitations honest?
- Does the README clearly connect to EEG, BCI, and neurotechnology?
- Can another developer reproduce the work?

## Final Delivery Format

When the implementing agent finishes, it should report:

- Files created.
- Dataset used.
- Subjects and runs analyzed.
- Figures generated.
- Report path.
- Tests or reproducibility checks performed.
- Known limitations.
- Recommended next repository step.
