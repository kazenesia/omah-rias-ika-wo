---
name: token-optimizer
description: Token optimization for Antigravity (Google's AI coding assistant). Reduce ghost tokens, prevent context compaction, track quality degradation, and optimize context window usage.
---

# Token Optimizer – Antigravity Edition

## Overview

Antigravity, like other LLM coding assistants, suffers from ghost tokens, context compaction, and quality drift. Token Optimizer is a methodology and toolkit originally built for Claude Code, OpenCode, and Codex – but its core principles apply directly to Antigravity.

This skill provides Antigravity users with practical strategies to:
- Identify and remove structural waste (unused context, stale memories, duplicate configs)
- Prevent information loss during context compaction
- Monitor session quality with signal-based scoring
- Recover up to 70% of context lost per compaction

## Why Antigravity Needs Token Optimization

Antigravity maintains a context window that can fill with:
- **Unused tool definitions** – Declared but never invoked
- **Stale project memories** – References to deleted files or outdated patterns
- **Bloated terminal outputs** – Large `cat`, `ls -laR`, or build logs
- **Redundant system instructions** – Duplicate rules across multiple config files

Without optimization, each compaction discards 60-70% of prior context, forcing Antigravity to re-learn project state.

## Core Concepts

### Ghost Tokens
Hidden tokens that consume context without value. In Antigravity, common sources:
- Orphaned entries in `.antigravity/memory.md`
- Tool schemas for disabled integrations
- Repeated context from long terminal histories
- Stale file references

### Compaction Checkpoints
Token Optimizer saves progressive checkpoints at fill bands (20%, 35%, 50%, 65%, 80%) and milestones (pre‑complex edit, pre‑multi‑tool sequence). After compaction, relevant checkpoints restore lost information.

### Quality Scoring (7‑Signal)
Adapted for Antigravity:

**ResourceHealth (monotonic – only decreases in a session)**
- Context fill degradation – how quickly you approach limit (50%)
- Compaction depth – number of times context was compressed (30%)
- Waste token ratio – stale reads + unused outputs (20%)

**SessionEfficiency (rolling window – can improve)**
- Stale reads – reading files you just wrote (30%)
- Bloated results – large outputs never referenced (30%)
- Decision density – ratio of meaningful turns to filler (20%)
- Tool efficiency – actions per token spent (20%)

Grades: S (90+), A (80+), B (70+), C (55+), D (40+), F (<40)

## Waste Categories in Antigravity

| Category | Typical Share | Examples |
|----------|---------------|----------|
| Unused context files | 10-20% | `.antigravity/rules/*.md` never loaded in last 30 sessions |
| Duplicate instructions | 15-25% | Same rule in both `antigravity.json` and `AGENTS.md` |
| Stale memories | 10-15% | Memory entries pointing to deleted paths |
| Tool output waste | 20-30% | `cat` of 10MB JSON, `git diff --cached` on large repos |
| Compaction debris | 5-10% | Residual tokens from previous compactions |

## Structural Fixes (Zero Quality Loss)

These removals are completely safe – they delete only unused components.

### 1. Prune Unused Context Files
```bash
# List all rule files in Antigravity
ls .antigravity/rules/

# Check which were actually loaded in recent sessions
# (Antigravity logs to ~/.antigravity/logs)
grep "loaded rule" ~/.antigravity/logs/* | cut -d: -f2 | sort | uniq -c

# Remove any rule file with zero loads over 30 days
rm .antigravity/rules/unused-rule.md