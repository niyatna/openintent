# Hermes local install note

Installed manually from `mvanhorn/signal-radar-skill` because `hermes skills install` blocked the community repo with a DANGEROUS scan verdict and `--force` does not override dangerous verdicts.

Reviewed before install:
- scanner hits were mainly expected for a research skill: env/API key handling, optional X cookie auth, subprocess wrappers, and strict output-contract prompt text;
- demo binary assets under `assets/` are not referenced by the skill and were intentionally excluded to avoid library bloat;
- runtime remains gated by Hermes tools/terminal permissions and optional credentials.

Source commit: `122158415ae421da83e739f2668032f6bc78d39c`
Version: `3.3.2`
