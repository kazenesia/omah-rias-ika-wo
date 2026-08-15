# Framework Guide: 3-Tier Workflow

This project follows the **Nerra.id Agentic Framework** as defined in [AGENTS.md](../../AGENTS.md).

## Workflow Overview

### Tier 1: The Blueprint (Directives)
- **Location:** `docs/directives/`
- **Purpose:** Standard Operating Procedures (SOPs).
- **Maintenance:** Update these files whenever a workflow is improved or a common bug is found.

### Tier 2: The Brain (Orchestration)
- **Role:** AI Agent (Antigravity).
- **Responsibility:** Parse directives, trigger execution scripts, handle errors, and manage the overall flow.

### Tier 3: The Muscle (Execution)
- **Location:** `scripts/`
- **Purpose:** Deterministic Python scripts for data crunching, API requests, and complex logic.
- **Rules:** Must be fast, reliable, and heavily commented.

## Directory Map

- `docs/directives/`: Markdown instruction manuals.
- `scripts/`: Deterministic Python scripts.
- `.tmp/`: Disposable temporary data.
- `.env`: Local environment variables (do not commit).

## Protocols

1. **Search Before You Build:** Always check `scripts/` for existing scripts.
2. **Auto-Correction:** Fix execution scripts immediately upon error.
3. **Evolve Blueprints:** Directives are living documents. Improve them constantly.
