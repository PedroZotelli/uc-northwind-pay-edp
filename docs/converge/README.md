# Converge — the document factory

Empty on purpose. This is the spine the room walks **with** the instructor.
Nobody arrives to a filled factory. Brownfield here means: the **legacy use
case** already runs; the **descent** has not started.

The method is Converge, end to end. Task-Spec, Seamwise (the Structure and
Decompose cuts), and Brief-Spec show up as named tools **inside** a pass.
They do not get their own tree.

```text
Capture → Intent → Structure → Decompose → Consensus
       → Tasking → Register → Harness → Loop
```

Every pass lowers altitude, binds an engine, and ends at a gate. The Loop
does not lower — it closes. Converged means an eval passed, not that anyone
felt done.

| Pass | Folder | Enters | Exits (the room writes this) |
|---|---|---|---|
| 0 | [`00-capture/`](00-capture/README.md) | raw idea, if there is no brief | signed BRD — or a no-go |
| 1 | [`01-intent/`](01-intent/README.md) | the brief | tech-spec that answers it |
| 2 | [`02-structure/`](02-structure/README.md) | tech-spec + the running oracle | ADRs: facts and constraints, never how to build |
| 3 | [`03-decompose/`](03-decompose/README.md) | ADRs | swimlane plans (plan altitude only) |
| 4 | [`04-consensus/`](04-consensus/README.md) | those plans | plans that survived an adversary |
| 5 | [`05-tasking/`](05-tasking/README.md) | hardened plans | Task-Specs under [`tasks/`](../../tasks/README.md) |
| ① | [`06-register/`](06-register/README.md) | Task-Specs | one spec = one issue (when a tracker is on) |
| 6 | [`07-harness/`](07-harness/README.md) | the stack | control plane (`AGENTS.md`, rules) |
| 8 | [`08-loop/`](08-loop/README.md) | a ready issue | green eval → PR |

Reference manuals (not this factory) live one level up: `cvg-aut-systems-spine-steps-v5.pdf`, `task-spec-v3.2.0.pdf`, `asd-agentic-loop-v1.0.html`.

Prior-run ADRs (`docs/decisions/001`–`011`) were removed from this tree so
Day 1 cannot copy last time’s answers. They remain in git history.
