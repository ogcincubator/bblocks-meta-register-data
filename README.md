# OGC Building Blocks Meta-Registry

A central index that maps short aliases (e.g. `@ogc/main`) to OGC Building Blocks register URLs,
so that `bblocks-config.yaml` imports stay stable even when registers move hosts.

The compiled index is published at:

```
https://w3id.org/ogc/bblocks/meta-register.json
```

## Published artifacts

| URL | Description |
|---|---|
| `https://w3id.org/ogc/bblocks/meta-register.json` | Flat alias map: `{ "@org/name": "https://..." }` |
| `https://w3id.org/ogc/bblocks/meta-register-orgs.json` | Organisation metadata: name, description, URL, maintainers, register list |

The `default` key in `meta-register.json` resolves to `@ogc/main` and is used by tooling that has not yet been configured with an explicit alias.

## How it works

Each organisation or user claims a namespace by adding a directory under `registers/` with a
`registers.yaml` file. On every merge to `master`, the index is recompiled and published to
GitHub Pages via the w3id.org persistent URL above.

In `bblocks-config.yaml`, instead of a raw URL:

```yaml
imports:
  - https://raw.githubusercontent.com/acme-org/my-bblocks/main/build/register.json
```

you write:

```yaml
imports:
  - "@acme/my-bblocks"
```

## Registering your building blocks

### 1. Fork this repository

Fork [ogcincubator/bblocks-meta-register-data](https://github.com/ogcincubator/bblocks-meta-register-data)
and create a branch for your changes.

### 2. Create your namespace directory

Add a directory named after your GitHub organisation or username under `registers/`, with a
`registers.yaml` file:

```
registers/
  your-org/
    registers.yaml
```

### 3. Fill in `registers.yaml`

```yaml
org:
  name: Your Organisation Name
  url: https://your-org.example.com
  maintainers:
    - github: your-github-username
      email: you@your-org.example.com

registers:
  my-register: https://your-org.github.io/my-bblocks/register.json
```

**Fields:**

| Field | Required | Description |
|---|---|---|
| `org.name` | yes | Full, human-readable organisation name |
| `org.description` | no | Short description of the organisation |
| `org.url` | yes | Publicly reachable URL for the organisation |
| `org.maintainers` | yes | At least one maintainer with `github` username and `email` |
| `registers` | yes | Map of register slugs to their `register.json` URLs (at least one) |

**Slug conventions:** lowercase, hyphens only, no `bblocks` prefix (e.g. `ogcapi-features` not
`bblocks-ogcapi-features`).

### 4. Verify locally (optional)

```bash
pip install pyyaml jsonschema
python .github/scripts/compile.py --validate
```

### 5. Open a pull request

Open a PR against `master`. The `validate` workflow will run automatically and check that your
`registers.yaml` is well-formed.

PRs adding a **new namespace** are reviewed by the maintainers of this repository.
PRs **modifying an existing namespace** must be authored by one of the maintainers listed in that
namespace's `registers.yaml`.

## Modifying an existing namespace

If you are an authorised maintainer of a namespace (listed under `org.maintainers`), you can open
a PR to add, update, or remove registers within your namespace. The same validation workflow
applies.

## Structure

```
registers/
  {org}/
    registers.yaml    ← one file per org/user namespace
.github/
  scripts/
    compile.py        ← compiles registers/ → index.json
  workflows/
    compile.yml       ← runs on merge to master, publishes to GitHub Pages
    validate.yml      ← runs on PRs, validates registers.yaml files
index.html            ← landing page served via GitHub Pages
```
