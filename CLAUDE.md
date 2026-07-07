# bblocks-meta-register-data

Meta-registry mapping short aliases (e.g. `@ogc/main`) to OGC Building Blocks
`register.json` URLs. See README.md for the full contributor-facing explanation.

## Source of truth vs. generated files

- `registers/{org}/registers.yaml` is the **source of truth**. Edit these files.
- `index.json` and `orgs.json` at the repo root are **generated** by
  `.github/scripts/compile.py` and published to GitHub Pages by
  `.github/workflows/compile.yml` on every merge to `master`. Do not hand-edit
  them — changes will be overwritten on the next compile.
- The `main`/`@ogc/main` entry (opengeospatial/bblocks) is the one register
  whose `register.json` lives at the repo root, not under `/build/`. Every
  other register's URL should point to `.../build/register.json`.

## Editing registers

When adding or fixing a register URL, edit the relevant `registers/{org}/registers.yaml`
and curl-verify the resulting URL returns 200 before committing.