# Shared implementation maintenance

The seven standalone packages intentionally bundle the same stdlib-only runtime; installation never depends on this catalog checkout. This directory holds the reviewed shared implementation and regression tests. Product-specific copy, prompts and source snapshots remain in their own repositories.

Before a coordinated release, compare the checked-out packages:

```bash
python3 verify_shared.py --repos-root /path/to/parent/of/seven/repositories
```

This command is read-only. For a runtime change, review the shared implementation, update the corresponding files in all seven packages, run the tests and actual provider probes, increment all manifests, then repin the reviewed release commits. Never overwrite unrelated or uncommitted work. Do not count repeated execution of the same 64 tests as 448 distinct tests.
