# Pass 2 — Structure

**Altitude:** system. This is where ADRs are born.

- Enters: the tech-spec, plus facts observed from the running legacy oracle.
- Exits: numbered ADRs in this folder. Facts and constraints. Never “how to build.”
- Gate: the system is understood well enough to cut seams.

Seamwise lives here: one concern, one record. A later ADR supersedes; nobody
rewrites an earlier one.

This folder starts empty. Day 1 fills it from the contracts and a live
`make run`, not from a previous factory’s answers.
