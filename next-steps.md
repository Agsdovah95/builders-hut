# Next Steps Plan

> **Date:** February 2026
> **Current State:** v0.4.3, `phase1` branch — 170 tests passing, 87% coverage

---

## Recommended Next Steps (in order)

### 1. Merge `phase1` tests to `main`
The test suite is passing and coverage is strong. The only gap is `cmd_interface.py` at 58% — but that's interactive UI code which is hard to unit test. Ship what you have.

### 2. Bump version to 0.5.0
Update version in both `pyproject.toml` and `cmd_interface.py` (APP_VERSION constant). Tests + quality foundation = milestone complete.

### 3. Implement `hut add` command (Phase 1.4)
This is **the highest-impact feature** to build next. Right now `add` is a stub in `cmd_interface.py`. It would make the tool genuinely useful day-to-day, not just at project creation time. Start with:
- `hut add crud <name>` — full stack (model + repo + service + schema + endpoint)
- `hut add model <name>` / `hut add endpoint <name>` — individual components
- Auto-update `__init__.py` imports and router registration

### 4. Complete NoSQL/MongoDB support (Phase 1.3)
The database factory pattern is already in place. You need:
- MongoDB connection template (`motor` async driver)
- MongoDB document models (no Alembic needed)
- MongoDB repository pattern
- Wire it through `DatabaseFactory`

### 5. DX improvements (Phase 1.5) — quick wins
These are small but make the tool feel polished:
- `--dry-run` flag (preview what would be created)
- `--verbose` flag
- Python version validation (currently says 3.13+ but roadmap wants 3.11+)
- Better error messages on subprocess failures

### 6. Then move to Phase 2 — start with Docker (2.2)
Docker support is the easiest Phase 2 item and adds huge value — it's just template files (`Dockerfile`, `docker-compose.yml`, `.dockerignore`). No complex logic needed. Good stepping stone before tackling auth.

---

## What to skip or defer

| Item | Why defer |
|------|-----------|
| Documentation overhaul (1.2) | README is already decent. Polish it when you hit 1.0 |
| Auth system (2.1) | Large scope — save for after `hut add` exists so users can `hut add auth` |
| Plugin system (3.1) | Post-1.0 territory |

---

**TL;DR:** Merge tests → bump to 0.5.0 → build `hut add` → finish MongoDB → then Docker. The `hut add` command is the single biggest value-add to ship next.
