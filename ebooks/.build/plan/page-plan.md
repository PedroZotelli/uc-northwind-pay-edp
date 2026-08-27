# ebook-converge page plan (authoritative coverage map)

Source of truth: `ebooks/brf-converge.md` (1357 lines). Every page below lists the facts that MUST
appear verbatim-accurate. Page IDs P01..P83. One page = one `.slide` section = one PDF page at
1440x900. Do not drop pages. Do not invent facts; everything on a page must trace to the brief.

Semantics (from §3 — these OVERRIDE the task-spec kit's gold-brand habit):
- Contract Purple `#A78BFA` = Converge itself (sequencing, binding, contracts) — the BRAND accent.
- Human Gold `#F3B64C` = human authority only (topology acceptance, barrier, key-holder). Never decorative.
- Seam Cyan `#68C7FF` = Seamwise topology / TaskPlan / lineage / decomposition.
- Accepted Green `#3DDC97` = verified gates, acceptance, receipts, settlement.
- Refused Red = stale review, tamper, scope escape, refutation, unsupported claim.
- Observer White/warm gray = Cockpit / read-only projections; never authority gold.
- Dotted lines = optional/opt-in routes or non-authoritative observation only.

---

## FRONT MATTER (P01–P07)

### P01 — Cover · CONVERGE
- src: S01, §1. HUD: `CONVERGE · TITLE`.
- Wordmark `CONVERGE` (violet gradient), tag "the factory coordinator for agentic delivery",
  Converge icon (`assets/converge-icon.svg` copied into build), Settlement Fold lockup.
- Core line: "Coordinate intent, decomposition, task authority, execution, and settlement —
  without duplicating authority."
- Folded rail visual: `intent → topology → contract → execution → evidence`.
- Proof token: `cvg 0.2.0 (task-spec 3.8.0)`. Edition line: "The Converge System — Canonical Ebook · Converge 0.2.0".
- Sub: "An end-to-end technical book: nine passes, two phases, one human barrier."

### P02 — North star: the referee, not the player
- src: §1. Quote block: "Converge is the factory coordinator and assurance layer around independent
  decomposition and task-contract engines… It is the referee, not the player."
- Visual: authority-chain mermaid from §1 (Intent+evidence → Seamwise → TaskPlan/v1 → Converge →
  Task-Spec → Converge bind → Executor → Task-Spec acceptance → Converge settlement receipts;
  Human reviewer / Human key holder gold nodes). classDef colors per brief.
- Emotional arc strip, 7 beats: Unease · Separation · Descent · Barrier · Bounded motion · Settlement · Honesty.

### P03 — The evidence ladder
- src: §2. Nine ranks as a ladder/table: A Authority, C Contract, I Implemented, T Tested,
  E Evidence, R Release, D Documentary, W Working tree, F Future — each with its surface paths and
  deck-use rule. Message: "A polished README, a green leaf test, and an immutable release receipt
  are not interchangeable evidence."
- W rank must be visibly labeled `CHECKOUT ONLY`; F = "never render as current capability".

### P04 — The audit snapshot
- src: §2. Two tables: (1) tracked paths — skills 220, apps 102, evidence 72, tests 22, assets 21,
  docs 18, scripts 11, bin 7, .github 7, contracts 6; total 508. Baseline `58b1ddb` = origin/main;
  `v0.2.0` tag `3de9f0b` is 42 commits behind; checkout expands CLI matrix 57 → 60 forms.
  (2) Direct validation 2026-08-26: runtime contract 48/48; register 145/145; loop kernel 57/57;
  passes 0–4 = 39+24+38+33+23 rows; conductor checkout 44/44; clean room 21/21; compose 14/14;
  JSON envelope 25/25; JSON matrix 60 forms/239 calls; docs/package `DOCS=READY files=22 commands=60`,
  `PACKAGE=READY files=244 skills=11`; Cockpit 40 server + 62 client; retained evidence 20 files;
  archived assets 6/6 on v0.1.0; demo `LOCAL_SETTLED`, `ACCEPTED=1`, `DEMO_COMPOSED=READY`.
- RED load-bearing callout: aggregate `make check` FAILS — `tests/test-repo-layout.sh` rejects tracked
  `AGENTS.md` + `OPERATING.md` as undeclared top-level files. Subsystems passed; release-ready may NOT be claimed.

### P05 — What may be claimed, what must be refused
- src: §2. Two columns. May (12 items): thin factory coordinator around independently versioned
  Seamwise/Task-Spec binaries; one authority per decision (duplicate capability tolerated, duplicate
  authority not); nine passes/two phases/one barrier/optional Capture/opt-in Register; materialization
  never authorizes dispatch (`dispatch_authorized: false`); `gate --stamp` is the only sealing action;
  bind adds repo fence possibly stricter than task scope; loop chooses no work (one named issue,
  finite budgets); default isolation = Git worktree, settled work survives on task branch; eight
  distinct terminal outcomes; Task-Spec performs independent acceptance; Cockpit/Ask cannot authorize
  or settle; release and current main are different evidence corridors.
  Refuse (11 items): everyday portfolio coordinator (= WorkHelm); owning Seamwise/Task-Spec internals;
  reviewed topology/materialization/receipt/narration authorizes execution; HMAC proves identity /
  hides key / sandboxes; bind prevents every out-of-scope write (some adapters detect post-fact);
  tier-2 holdouts are secret from the worker; LOCAL_SETTLED implies PR/remote/merge/production;
  Cockpit/Ask/`cvg next`/tracker as canonical state; Manager fleet/autonomous fan-out/live-tracker/
  production reliability in v0.2.0; guided chat + 60-form CLI as committed/released/hosted;
  current `make check` passes.

### P06 — The visual system (legend)
- src: §3. Semantic color table (7 roles, hex, use). Components: descent rail (passes 0–8, bypass
  rails for optional hops), barrier gate (Pass 4), contract fold (compose→seal→bind→loop→accept),
  receipt stack (6 distinct cards), macOS code window (8–18 visible lines), solid connectors with
  arrowheads; dotted = optional/observation. Rules: never draw Cockpit/model arrows writing into
  canonical state; one authority/pass/boundary per page; ≤6 table rows on narrative pages;
  every green claim carries a named gate/receipt/test token; every red claim states refusal + safe next action.

### P07 — Story map + master transition
- src: §4. Acts table (7 acts, slide ranges 01–76, question answered, emotional move).
- Master transition mermaid: Ambiguous intent → Reviewed topology → Unsigned tasks → Sealed revision
  → Bound runtime → Finite loop → Independent acceptance → Scoped settlement.

---

## ACT I — ONE DECISION, ONE OWNER (P08–P14)

### P08 — S02 · Agentic delivery fails when authority becomes ambient
- HUD `THE PROBLEM · DUPLICATE AUTHORITY`. Core line per brief.
- Visual: four overlapping red circles (planner, coordinator, executor, observer) each claiming
  `APPROVED`; collapse into "one decision / one owner" cards.
- Four refusals on-page: model narration ≠ acceptance; tracker state ≠ authority;
  materialization ≠ dispatch; observation ≠ control.
- Sources [A] docs/concepts/authority.md; [D] docs/trust/index.md. Transition line per brief.

### P09 — S03 · It is a referee, not the player
- HUD `THE CATEGORY · THIN COORDINATOR`. Core line per brief.
- Visual: central purple referee plate, cyan engines (Seamwise, Task-Spec) on either side, scoped
  executor below. Table: Converge owns (cross-engine sequence, composition receipts, runtime
  binding, bounded loop + settlement) vs does not own (seam discovery, Task-Spec rendering, HMAC
  authorization, independent acceptance internals).
- Sources [A] OPERATING.md, authority.md; [I] bin/_cvg_compose.py, bin/cvg.

### P10 — S04 · Everyday work and factory work are different planes
- HUD `OPERATING MODEL · CONSULT VS FACTORY`. Two lanes: Everyday `human ↔ WorkHelm → engines`;
  Factory `human barrier → Converge → compose/bind/settle`.
- Boundary: neither lane skips the Task-Spec HMAC seal; neither merges the user branch automatically.
- Source [A] OPERATING.md.

### P11 — S05 · One decision, one owner
- HUD `AUTHORITY · SOLE OWNERS`. Five tall cards: Human reviewer (accepts topology/risk), human key
  holder (authorizes a leaf) — both gold; Seamwise (seams + lineage, cyan); Task-Spec
  (materialization/seal/evals/acceptance, cyan); Converge (sequencing/bind/settlement, purple);
  Executor (product-code change, neutral). Cockpit OUTSIDE the write rail (observer white, dotted).
- Line: "Duplicate capability is tolerable. Duplicate authority is not." Source [A] authority.md.

### P12 — S06 · Follow one feature, not nine abstract passes
- HUD `THE STEEL THREAD · HEALTH ENDPOINT`. Specimen card `T-20260815-health-status` travels through
  states: topology accepted → materialized unsigned → HMAC sealed → bound → RED/GREEN → accepted →
  local settlement. Explain this card reappears across the book.
- Sources [D] README.md; [T] scripts/demo-composed.sh.

### P13 — S07 · Six receipts, six different claims
- HUD `EVIDENCE · DO NOT FLATTEN THE STACK`. Receipt stack: review record (accepted topology),
  composition receipt (materialized), HMAC seal (authorized), runtime contract (bounded), execution
  receipt (executed), acceptance record (accepted) — one verb each.
- Red callout: `composition receipt ≠ authorization`; `execution receipt ≠ acceptance`.
- Sources [C] contracts/converge-composition-receipt-v1.schema.json; [E] evidence/releases/v0.2.0/live-codex/.

### P14 — S08 · Nine passes, two phases, one barrier
- HUD `THE METHOD · WHOLE SPINE`. Full descent rail: `0 Capture → 1 Intent → 2 Structure →
  3 Decompose → 4 Consensus → 5 Tasking → 6 Register → 7 Bind → 8 Loop`; Pass 4 barrier gate;
  bypass rails around 0 (usable BRD skips Capture) and 6 (repo-local queue skips Register).
- Labels: "Design above the barrier. Machine build below it. Capture is optional; Register is opt-in."
- Sources [D] docs/guides/descent.md; [I] skills/evidence-to-next-pass/scripts/next-pass.sh.

---

## ACT II — THE HUMAN DESCENT (P15–P24)

### P15 — S09 · Design above. Build below.
- HUD `THE DESCENT · TWO PHASES`. Split-stage descent: passes 0–4 (gold/cyan human design) above the
  barrier, 5–8 (purple/green machine build) below. Boundary: "machine-led" ≠ self-authorized — the
  HMAC seal still belongs to Task-Spec + explicit key holder.
- Sources [D] descent.md; [A] OPERATING.md.

### P16 — S10 · FAST, NORMAL, FULL route work; they do not erase proof
- HUD `ROUTER · NOT A PASS`. Three rails merging at Tasking; red floor beneath all three.
- `cvg lane` changes ceremony, model tier, verification defaults within hard floors; cannot widen a
  signed budget or waive a gate. FAST may enter at Pass 5; NORMAL skips optional ceremony; FULL
  enables tier 2 by default. Sensitive/greenfield floors can force a stronger lane.
- Sources [I] bin/cvg-classify-lane.py, skills/task-loop/scripts/loop-kernel.sh; [T] runtime/loop suites.

### P17 — S11+S12 · Pass 0 Capture + frontier rounds
- HUD `PASS 0 · CAPTURE · OPTIONAL`. Fork: one idea card → `BRD` or `NO-GO`. Gate `CHECK_BRD=PASS`;
  draft mode may explain gaps but never authorizes. "Capture is an interview, not a summarizer."
- Frontier rounds: ask every currently unblocked question together; dependency graph of unknowns,
  only unblocked nodes glow; wait once, recompute. Checks: quantified pain, KPI-shaped goal, in/out
  scope, provenance, owner, open questions, canonical sign-off.
- Sources [I] skills/idea-to-brd/; [T] 39/39 Pass 0 rows.

### P18 — S13 · The do-nothing test is a kill switch
- HUD `PASS 0 · NO-GO IS A RESULT`. Balance visual: cost-of-action vs cost-of-inaction; no-go receipt
  exits the descent. "If inaction has no meaningful cost, stop manufacturing a project."
- Boundary: a no-go must be durable, owned, dated, specific — not model reluctance.
- Sources [I] Pass 0 templates and tests.

### P19 — S14+S15 · Pass 1 Intent + altitude
- HUD `PASS 1 · INTENT`. BRD claims → interrogate/crystallize gates → numbered falsifiable
  requirements. Gate `CHECK_TECH_SPEC=PASS`; unsigned, pending, open blockers, invalid dates,
  ambiguous inputs fail closed.
- Altitude diagram: owner problem → requirement → forbidden premature solution (red). Implementation
  leakage may warn; unresolved blockers still block. "Requirements say what must be true. They do
  not choose architecture."
- Sources [I] skills/brd-docs-to-tech-req/; [T] 24/24 rows.

### P20 — S16+S17 · Pass 2 Structure + terrain altitude
- HUD `PASS 2 · STRUCTURE`. Requirement cards pinned on a repository terrain map. Gate `CHECK_ADR=OK`;
  final mode rejects proposed ADRs, dangling supersedes, empty evidence, missing context.
- Red/green verb wall: record what is true (green) vs `build, create, implement, refactor, migrate`
  (red — next pass). ADR structure: Context, Decision, Evidence, Consequences, status, supersession,
  glossary.
- Sources [I] skills/tech-req-to-adrs/, scaffold-adr.sh; [T] 38/38 rows.

### P21 — S18+S19 · Pass 3 Decompose + grammar
- HUD `PASS 3 · DECOMPOSE`. Monolith splits into seams → owning swimlanes → capability legs.
  Gate `CHECK_PLAN=OK`; no Mermaid, no non-goals, no legs, orphan legs, missing proof all fail.
- Grammar: seam separates responsibility; swimlane owns it; leg names an observable capability state.
  One owner per seam; dependency arrows between legs. A leg is NOT yet an atomic Task-Spec; real task
  IDs here = altitude drift.
- Sources [I] skills/reqs-to-swimlane-plans/; [T] 33/33 rows.

### P22 — S20 · Pass 4 · A different-family model tries to break the plans
- HUD `PASS 4 · CONSENSUS`. Primary-family plan enters cross-family adversary chamber; objections
  fan out. Gate `CHECK_CONSENSUS=OK`; self-review, no objections, no decider, open residual risk fail.
- "Refutation in. Hardened plans, objection log, owners, decisions, and residual risk out."
  "Dispatching the adversary does not close the pass."
- Sources [I] skills/sketch-plans-adversarial-review/; [T] 23/23 rows.

### P23 — S21 · An objection exists until a human decides it
- HUD `PASS 4 · RESOLUTION`. Objection cards must cross `DECIDED_BY` before reaching the barrier;
  adversary proposes, a named human decides FIX or ACCEPT and owns residual risk.
- Boundary: a fresh review log with unresolved findings is evidence of scrutiny, not consensus.
- Sources [I] `cvg review --resolve`, consensus gate.

### P24 — S22 · Consent binds the reviewed bytes
- HUD `THE BARRIER · HASHED CONSENT`. Plan digest stamped at review; mutated bytes turn the gate red
  and route back to re-attack. "If a reviewed plan changes, the barrier reopens. Consent does not
  transfer to new text."
- Proof: conductor tests discriminate matching hashes from post-review changes and refuse Pass 5
  behind stale consent (44/44 conductor checkout rows).
- Sources [I] consensus gate and conductor.

---

## ACT III — COMPOSE AND TASKING (P25–P35)

### P25 — S23 · Converge composes external engines; it does not vendor them
- HUD `COMPOSE · ENGINE BOUNDARIES`. Process boundary diagram: Seamwise + Task-Spec as independent
  binaries, JSON/CLI bridges, no shared implementation box. Checks: Seamwise must deny
  materialization/dispatch authority; Task-Spec must return supported result contract + version 3.8.x.
- Sources [A] authority.md; [I] bin/_cvg_compose.py; [T] compose suite.

### P26 — S24 · Compose has five named states and one safe next action
- HUD `COMPOSE · STATE MACHINE`. Mermaid stateDiagram-v2 (library C): [*]→NEEDS_REVIEW (prepare),
  NEEDS_REVIEW→PREVIEW_READY (named review), PREVIEW_READY self-loop (preview), →MATERIALIZED
  (materialize), MATERIALIZED self-loop (byte-identical rerun), red exits to BLOCKED from all three
  (stale/missing evidence, plan or review drift, task or receipt drift), [*]→ENGINE_UNAVAILABLE
  (version/capability failure).
- Status re-hashes evidence and emits exactly one `NEXT=` action; status is read-only.
- Sources [D] compose-and-settlement.md, recovery.md; [I] composer.

### P27 — S25+S26 · Prepare creates a delivery plan; review records one named acceptance
- HUD `COMPOSE · PREPARE + REVIEW`. Left: `cvg compose prepare --source recipe.yaml` asks Seamwise
  for topology, lands at NEEDS_REVIEW; Task-Spec disconnected; prepare does not compile a TaskPlan,
  record acceptance, or create Markdown leaves. Right: reviewer + substantive reason move topology
  to PREVIEW_READY; human card signs delivery-plan digest; compiler stays locked; no anonymous
  reviewer, no empty reason, no silent acceptance. Review performs no compilation.
- Sources [I] composer; [T] compose rows.

### P28 — S27 · Preview crosses the engine boundary without writing leaves
- HUD `COMPOSE · PREVIEW`. Lineage + TaskPlan cross a contract bridge into `taskspec plan`; output is
  a read-only proposed DAG. Seamwise compiles TaskPlan/v1; standalone Task-Spec validates/previews;
  NO Task-Spec Markdown written. Preview fails if review missing or Task-Spec unavailable.
- Sources [I] composer; [T] compose suite.

### P29 — S28 · Materialize writes unsigned tasks and the receipt last
- HUD `COMPOSE · MATERIALIZE`. TaskPlan → Task-Spec leaves → composition receipt, receipt pen held
  until bytes settle. Interrupted finalization recovers idempotently; exact rerun is byte-identical.
- Sources [I] composer; [T] 14/14 compose rows.

### P30 — S29 · The composition receipt is non-authorizing by contract
- HUD `COMPOSE · RECEIPT`. Annotated `ConvergeCompositionReceipt/v1` JSON card (use §8 specimen:
  contract, `dispatch_authorized: false`, source_commit, task_plan_digest sha256, task_ids
  [T-20260815-health-status], task_digests). Binds engine versions, source commit, lineage, plan
  digest, task IDs + digests.
- Red callout: a valid receipt proves materialization integrity — not permission to run, not
  acceptance after running.
- Sources [C] composition schema; [E] release receipt.

### P31 — S30 · Creation never grants authority
- HUD `TASK LIFECYCLE · UNSIGNED BY DEFAULT`. Task-Spec card with `signed_off: false`,
  `accepted: false`, locked execution rail. "Materialized means inspectable, not runnable."
  Seamwise review and Converge materialization are upstream evidence; neither may flip the seal.
- Sources [A] authority docs; [T] compose materialization authority row.

### P32 — S31+S32 · Pass 5 Tasking + `tasks plan` dry run
- HUD `PASS 5 · STANDALONE TASK-SPEC`. Accepted capability legs → atomic leaves with runnable evals,
  dependency closure, scope, budgets, acceptance criteria; one capability leg expands into a small
  Task-Spec DAG. Converge offers compatibility doors under `cvg tasks *`; delegates directly to the
  external engine (route_taskspec() in bin/cvg).
- `tasks plan` is a dry run, not a second decomposer: derives proposed units from the TaskPlan,
  never invents work to fill a missing leg; empty yield stays visibly empty; read-only, forwards the
  standalone TaskPlan unchanged. Proof `TASKS_PLAN_TESTS=PASS`.
- Sources [A] authority.md; [I] bin/cvg.

### P33 — S33 · HMAC authorization binds one exact revision
- HUD `PASS 5 · TIER 1`. TaskRevision enters PRE; HMAC envelope + `TIER=1` exit.
  `taskspec gate --stamp` sets `signed_off: true` only after validating the exact body digest under
  the repository key. Boundary: HMAC is tamper evidence under a shared key — NOT identity, secrecy,
  isolation, or semantic truth.
- Sources [A] OPERATING.md; [D] docs/trust/index.md; [T] clean-room and version checks.

### P34 — S34+S35 · Pass 6 Register + parity contract
- HUD `PASS 6 · REGISTER · OPTIONAL`. One signed Task-Spec becomes one tracker issue; `blocked-by`
  mirrors the DAG; repository files remain canonical; dotted non-authoritative projection lines.
  Pass 6 authors no tasks, changes no dependency truth, may be skipped for a repo-local queue.
- Parity: count, identity, dependency edges, receipts, landed-task history must agree. 5 specs ↔ 5
  issues one-to-one; orphan/missing/cycle/dangling glow red. Idempotent reruns update in place;
  cycle/dangling preflights write no half-board; receipt stamping preserves the HMAC payload.
- Sources [I] skills/task-specs-to-issues/; [T] 145/145 register rows.

### P35 — S36 · Tracker writes are capability-gated and fail-soft
- HUD `PASS 6 · EXTERNAL EFFECTS`. Capability envelope controlling `tracker.write`; config and
  projection lock carry `0600` badges; symlinked local state refused. Identity, projection structure,
  and tracker mutation are separate decisions with private machine-local state. Adapter failure is
  reported; it must not rewrite the task-loop verdict.
- Sources [I] register/setup code; [T] register and install suites.

---

## ACT IV — BIND THE RUNTIME (P36–P42)

### P36 — S37+S38 · Pass 7 Bind + input freshness
- HUD `PASS 7 · BIND`. One signed Task-Spec → one execution profile + guards, adapters, worker brief;
  sealed revision folded into `7A contract` and `7B brief`. Gate `CHECK_RUNTIME_CONTRACT=PASS`.
- Freshness: seal, body digest, backend, evidence, task identity must still agree; mutated body and
  runtime drift hit red gates. `bind --check` re-verifies without writing; a task moved to
  `tasks/done` remains verifiable by identity. A stale or unsigned task never reaches runtime selection.
- Sources [I] skills/task-to-runtime-contract/; [T] 48/48 runtime checks.

### P37 — S39 · The runtime contract carries enforcement, not duplicated prose
- HUD `PASS 7 · EXECUTION PROFILE`. Annotated execution-profile YAML card: pinned task revision,
  backend, topology, budgets, evidence slice, path policy, capabilities, authority epoch. The profile
  references the task; it does not become a second task contract.
- Sources [I] bind templates/scripts; [T] thin/portable/deterministic checks.

### P38 — S40 · The repository gate outranks a task that asks for too much
- HUD `PASS 7 · TWO FENCES`. Outer Task-Spec write scope (candidate set) and smaller inner repository
  fence (trusted policy may narrow; protects itself from deletion or weakening). Mermaid D (binding
  fences) may anchor this page. Proof: nested projects inherit Git-root policy; renames include both
  endpoints; whole-repo diff catches sibling changes; invalid policy fails closed.
- Sources [I] check-gate.py; [T] gate-policy tests.

### P39 — S41 · Prevent and detect are different control classes
- HUD `PASS 7 · ENFORCEMENT HONESTY`. Preflight shield vs postflight tripwire. Codex may prevent
  some writes before the tool call; Claude and Kimi often detect violations postflight. The resolver
  manifest records the class; documentation may not upgrade `detect` to `prevent`.
- Sources [D] docs/trust/index.md; [I] runtime adapters; [T] enforcement/waiver checks.

### P40 — S42+S43 · Intra-task topology + 7B worker brief
- HUD `PASS 7 · TOPOLOGY + BRIEF`. Single is the default; parallel requires substantive evidence and
  disjoint ownership (write sets do not overlap); topology never creates new task authority or
  cross-task scheduling. 7B emits `AGENTS.task.md`: identifiers, epoch, scope, proof route, source
  contract — not a rewritten implementation plan; stale brief fails the gate; generic router setup
  proposes beside human content and never clobbers it.
- Sources [I] bind topology logic, task-brief/scaffold scripts; [T] non-single/disjointness, 7B and
  non-clobber rows.

### P41 — S44 · Adapters are execution bridges, not new authorities
- HUD `PASS 7 · CODEX · CLAUDE · KIMI`. One profile feeding three adapter sockets; all return to the
  same verification rail. An adapter selects a declared runtime, closes stdin, filters environment,
  reports what it can enforce. Proof: explicit engine/profile mismatch fails before execution; all
  three receive closed stdin.
- Sources [I] engine adapters; [T] runtime and loop suites.

### P42 — S45+S46 · Commit the contract + `bind --check` last preflight
- HUD `PASS 7 · COMMIT + CHECK`. Dirty main tree fades; committed sealed task + execution profile
  appear inside a fresh worktree (isolation sees committed state only). Committing the contract is
  not merging product work or opening a PR. Then: five inputs (task, profile, policy, evidence,
  runtime capabilities) converge on `CHECK_RUNTIME_CONTRACT=PASS` — re-hash without changing the
  repository; direct test verifies zero writes + current freshness.
- Sources [D] bind-and-loop.md; [I] loop kernel, checker.

---

## ACT V — THE LOOP AND SETTLEMENT (P43–P54)

### P43 — S47 · Pass 8 runs one named issue; it never selects the frontier
- HUD `PASS 8 · THE LOOP`. `cvg loop --issue …` receives one assignment; issue enters a single loop
  cell; future fleet silhouette stays outside the product boundary (Manager/fleet scheduling outside
  v0.2.0). No issue ID = usage error; Pass 8 may not invent or fan out tasks.
- Sources [I] loop kernel; [D] README scope.

### P44 — S48 · Fresh process per attempt; state lives on disk
- HUD `PASS 8 · FRESH CONTEXT`. Agent bubbles disappear each iteration; disk artifacts persist
  (spec, diff, Git history, checkpoint, attempt log). Previous-failure context is bounded and
  explicit; hidden chat memory is not loop state.
- Sources [I] loop-kernel.sh; [D] loop-spec.md.

### P45 — S49 · Three budgets fail differently
- HUD `PASS 8 · FINITE SPEND`. Three gauges (iterations, working time, tokens) under a hard signed
  ceiling; a CLI flag may tighten, never raise, the signed maximum. `--resume` continues accumulated
  working time, not wall time paused. Missing token budget reported as unbounded, never guessed.
- Sources [I] loop kernel; [T] budget rows.

### P46 — S50 · Lane chooses model cost and verification defaults
- HUD `PASS 8 · COST DIAL`. Lane × effort matrix → model tier, reasoning, timeout, verification.
  FAST does not draw the largest model; FULL enables tier 2; effort scales per-attempt time.
  Explicit `--no-verify` can override FULL; no lane widens signed budgets.
- Sources [I] loop kernel; [T] lane rows.

### P47 — S51 · Worktree isolation is the default safety posture
- HUD `PASS 8 · ISOLATION`. Main checkout left, temporary worktree right, task branch below. Landing
  rules: SETTLED/LOCAL_SETTLED clean the duplicate worktree; BLOCKED/STALLED/EXHAUSTED keep
  inspectable uncommitted work; failed empty runs clean up.
- Sources [I] loop kernel; [T] isolation/cleanup rows.

### P48 — S52+S53 · The kernel + stagnation breaker
- HUD `PASS 8 · KERNEL`. Mermaid E (loop kernel): checkpoint → fresh attempt → tier-1 eval + path
  gate; RED+budget → learn from bounded evidence → checkpoint; RED+stop → named failure landing;
  GREEN → tier 2 enabled? REFUTED → learn; UPHELD/policy-allows-unavailable → Task-Spec POST accept →
  receipt chain + settlement. On-slide order: checkpoint → attempt → tier 1 → path gate → tier 2 →
  acceptance → receipt.
- Breaker: repeated ineffective attempts land `STALLED` before the full budget burns; ineffective
  engine stops at three attempts rather than the declared fifteen.
- Sources [I] loop-kernel.sh; [T] loop suite, 57/57 loop rows.

### P49 — S54 · Eight terminal states make failure operational
- HUD `PASS 8 · LANDINGS`. Eight compact cards (the one allowed 8-card matrix): SETTLED (accepted,
  external publication allowed, exit 0), LOCAL_SETTLED (accepted, external writes denied, exit 0),
  NO_OP (already green at entry, exit 0), BLOCKED (human/upstream/tier-2 decision needed, exit 1),
  STALLED (stagnation breaker, exit 1), EXHAUSTED (signed budget reached, exit 1), CANCELLED
  (external stop, exit 1), ERROR (coordinator cannot continue safely, nonzero, safe failure).
  Work-preserved column per §7 terminal-states table.
- Sources [D] descent guide; [I] loop kernel.

### P50 — S55 · Tier 1 runs the sealed eval and the repository fence
- HUD `SETTLEMENT · TIER 1`. Eval result + path-policy result converge; either red blocks settlement.
  The declared Exit Check must go green AND the whole Git reality must remain inside policy.
  Boundary: a zero exit proves only the encoded claim on this host; it can be weak or gamed.
- Sources [D] trust docs; [I] gate/loop; [T] postflight rows.

### P51 — S56+S57 · Tier 2 refutation + holdout honesty
- HUD `SETTLEMENT · INDEPENDENT JUDGE` + `TRUST LIMIT · HOLDOUT`. Green eval enters adversarial
  chamber; judge sees intent, diff, holdout criteria; returns `UPHELD`, `REFUTED`, or unavailable.
  REFUTED loops back; UPHELD proceeds; an unobtainable verdict never becomes a pass — low-risk
  documented unavailability may proceed under policy; high-risk stops.
- Red honesty callout: the judge is intended to own `## Holdout`, but the worker brief still points
  at the Task-Spec that contains it. Do NOT say the worker could not read evaluator criteria.
- Sources [I] verify-work.py; [D] bind-and-loop.md, trust/index.md; [T] tier-2 loop rows.

### P52 — S58 · External writes default to deny
- HUD `SETTLEMENT · LOCAL FIRST`. Local task branch + receipt glow green; PR/tracker arrows locked.
  Without explicit `external_writes: allow` + capability grants, the loop settles locally and
  suppresses tracker/remote effects. Unauthorized tracker writes report `SKIPPED`; adapter failure
  reports `FAILED` without changing the loop landing.
- Sources [I] loop policy; [T] external-write rows.

### P53 — S59 · Acceptance belongs to Task-Spec
- HUD `POST · INDEPENDENT ACCEPTANCE`. Converge hands the exact revision + attempt back to Task-Spec;
  only `ACCEPTED=1` closes acceptance; AcceptanceRecord returns. Converge does not set
  `accepted: true` itself; worker narration and execution receipt are insufficient.
- Sources [A] authority docs; [I] acceptance routing; [T] clean-room path.

### P54 — S60 · Settlement is a hash-linked claim, not a victory message
- HUD `SETTLEMENT · RECEIPT CHAIN`. Mermaid F: review record → composition receipt (dispatch=false)
  → TaskAuthorization HMAC → runtime contract → execution receipt → AcceptanceRecord → settlement
  receipt, terminating green in `LOCAL_SETTLED` or `SETTLED`. Ten things must agree: spec, profile,
  handoff, eval, path policy, execution receipt, acceptance record, lifecycle ledger, commit, final
  status. Success receipt written after settlement; clean-room test verifies hash chain + ledger.
- Sources [E] release evidence; [T] runtime and clean-room suites.

---

## ACT VI — OPERATING SURFACES (P55–P63)

### P55 — S61 · `cvg next` reads the floor; it does not remember state
- HUD `CONDUCTOR · EVIDENCE TO NEXT PASS`. `cvg/` folders feed a read-only evidence board ending in
  `NEXT_PASS=N|DONE`. Artifacts reveal the current boundary; the conductor names the owning skill and
  gate; the gate still decides. Evidence presence is not verdict; stale Pass 4 hash displays `[!]`
  and blocks later passes.
- Sources [I] conductor skill/scripts; [T] conductor suite.

### P56 — S62 · Guided chat is checkout-only
- HUD `CHECKOUT ONLY · GUIDED CONTROL`. Large `W · NOT COMMITTED` ribbon. Uncommitted
  `cvg next --guided` adds `CONTINUE`, `EXPLAIN`, `INSPECT`, `PAUSE`, then waits — four choice cards
  above the same evidence board. No chat state persisted; silence never means continue; pre/post
  hooks and pass gates remain authoritative. Proof: 44/44 checkout conductor rows; matrix expands
  57 → 60 only in the dirty tree.
- Sources [W] guided-chat diff; [T] working-tree tests.

### P57 — S63 · Every public form speaks one JSON result contract
- HUD `CLI · MACHINE CONTRACT`. `ConvergeCLIResult/v1` specimen card (§8 JSON: contract, ok, token
  `COMPOSE=PREVIEW_READY`, verdict, exit_code, changed, dry_run, data, error, meta schema_version 1
  cvg_version 0.2.0). Global `--json` and `--dry-run` position-independent; exit code, token,
  mutation truth, error explicit. Proof: checkout matrix 60 forms / 239 calls; envelope suite 25 rows.
- Sources [C] CLI result schema/matrix; [T] JSON suites.

### P58 — S64 · Doctors name the broken hop, not only the missing tool
- HUD `OPERATIONS · DIAGNOSTICS`. Symptom chain: `missing shellcheck → gate blocked → unsigned task
  → bind refused → loop error`, doctor pointing at the first cause. Tokens `DOCTOR_HOST`,
  `DOCTOR_EVIDENCE`, `DOCTOR_PLUGIN`, runtime-contract result. Host, evidence, plugin,
  runtime-contract, and setup checks turn distant symptoms into one actionable upstream cause.
- Sources [I] doctor functions/scripts; [T] host/evidence/plugin suites.

### P59 — S65 · Install projects Converge into a consumer without embedding engines
- HUD `INSTALL · PINNED TOOL SURFACE`. One package fans out to `.agents/skills`, `.claude/skills`,
  `.grok/skills` (Codex/Kimi, Claude Code, Grok); Task-Spec and Seamwise binaries remain external.
  Copy mode pins 11 skills + CLI. Proof: 17 install checks + 21 clean-room checks green; local config
  `0600`, symlink-safe, idempotent, Git-excluded.
- Sources [I] install.sh, package.json; [T] install/clean-room suites.

### P60 — S66 · Eleven skills; Pass 5 remains external
- HUD `SKILLS · ROUTING SURFACE`. 11 skill tiles (eight pass skills + utilities
  `evidence-to-next-pass`, `pass-to-lesson`, `skill-creator`) around a separate Task-Spec engine
  tile; no mirrored Task-Spec skill. Proof: version unity finds exactly 11 skills at 0.2.0; package
  244 files, no vendored engine tree.
- Sources [C] package/plugin manifests; [I] skills; [T] version/package gates.

### P61 — S67 · Cockpit observes one canonical snapshot
- HUD `COCKPIT · READ-ONLY PROJECTION`. Full-screen Cockpit shell fed by `cvg snapshot`
  (`WorkspaceSnapshot 3.0`); NO write arrow returns (mermaid G usable here). Renders descent,
  decomposition, gates, queue, attempts, receipts, health, documents. Security: loopback only,
  explicit roots, token/exact-origin transport, GET-only, snapshot+SHA artifact allowlist,
  traversal/symlink/binary/credential rejection. Proof: 40 server + 62 client tests + production
  build green.
- Sources [I] apps/cockpit/; [C] snapshot schema; [T] Cockpit gate.

### P62 — S68 · Ask Converge is bounded interpretation over fresh evidence
- HUD `COCKPIT · ASK`. Artifact slice + redacted history enter an ephemeral ACP session; answer exits
  to the screen only. One snapshot-bound ACP turn can explain artifacts; it cannot create, approve,
  bind, transition, or settle them. Controls: fixed executable/argv/cwd/env, permission denial,
  unsafe-tool refusal, bounded history/output, cancellation, stale-turn rejection, credential redaction.
- Sources [I] Cockpit Ask services + ACP client; [T] server tests.

### P63 — S69 · Recovery follows tokens, not optimism
- HUD `OPERATIONS · ONE SAFE NEXT ACTION`. Compose/loop recovery table, one arrow per state: stale
  review → prepare/review again; interrupted materialize → rerun idempotently; EXHAUSTED → raise
  signed budget or split; REFUTED → fix work; CANCELLED → resume from handoff. Compose status emits
  one `NEXT=`; loop landings preserve the handoff and work a human needs.
- Gap callout: under worktree isolation, current `--resume` starts a fresh tree at attempt 1 — do not
  imply continuation of uncommitted work.
- Sources [D] recovery.md; [I] loop kernel.

---

## ACT VII — PRODUCT AND PROOF (P64–P70)

### P64 — S70 · Fifty-seven committed forms; sixty in the working tree
- HUD `CLI · SURFACE TRUTH`. 57 committed cards + 3 purple cards under a `W · CHECKOUT ONLY` bracket.
  Committed 0.2.0 main surface = 57 forms; audited dirty checkout adds 3 guided/conductor forms and
  tests 60. Never render 60 as released until committed + release evidence refreshed.
- Sources [C] committed/current matrix; [W] diff; [T] JSON matrix.

### P65 — S71 · The repository is an executable method, not one monolith
- HUD `REPOSITORY · MAP`. Repository map with source-of-truth arrows; counts: 508 paths, 220 skills,
  102 apps, 72 evidence, 22 tests, 18 docs, 11 scripts, 7 bin, 6 contracts. Distinct jobs: CLI,
  contracts, skills, observer, tests, scripts, evidence, templates, assets. Generated CLI reference
  comes from the command matrix; Cockpit from snapshot; tracker from Task-Spec — not the reverse.
- Sources [I] repository tree; [D] README map.

### P66 — S72 · Release, current main, and working tree are three corridors
- HUD `RELEASE · PROVENANCE`. Three parallel rails with hashes: release `v0.2.0` / `3de9f0b`
  (immutable), main `58b1ddb` (42 commits later), dirty checkout `58b1ddb + diff` (16 modified +
  1 untracked, uncommitted). Reported hosted evidence: README records all eight jobs green on feature
  SHA `1fa0545…` in run `32048296517` — repository-reported unless refreshed live.
- Sources [R] tag/workflow; [D] README; [W] Git status.

### P67 — S73 · The local evidence is strong and granular
- HUD `PROOF · WHAT PASSED`. Proof wall grouped by subsystem (no inflated total): Register 145,
  Loop 57, Runtime 48, Passes 0–4 (39+24+38+33+23), clean room 21, compose 14, JSON 60 forms/239
  calls, Cockpit 102 tests. Boundary: never sum overlapping suites into a fake universal count.
- Sources [T] direct 2026-08-26 outputs.

### P68 — S74 · Current-main `make check` fails at repository layout
- HUD `CURRENT GAP · AGGREGATE RED`. Green suite rail stops at a red `LAYOUT=FAIL` gate naming
  `AGENTS.md` + `OPERATING.md`. Exact failure: `tests/test-repo-layout.sh` reports both as undeclared
  top-level files; `make check` exits 2 before JSON/docs/compose/package phases — those phases pass
  when run independently. Safe remediation: update the declared layout contract or relocate the files
  through an explicit repository decision, then rerun the full aggregate gate.
- Sources [T] direct make check; [I] layout test.

### P69 — S75 · v0.2.0 proves a composed single-task path, not a factory fleet
- HUD `SCOPE · HONEST LIMITS`. Current capability island surrounded by named absent regions:
  production reliability, autonomous approval, live-tracker reliability, Manager scheduling not
  promised. Additional limits: private repository access; Task-Spec 3.8.x pin; Bash 4 needed for
  lint; HMAC key readability under weak confinement; holdout exposure; prevent/detect variation;
  NORMAL/FAST default local settlement without tier 2.
- Sources [D] README scope, trust docs, changelog; [A] operating contract.

### P70 — S76 · Sequence authority. Bind the attempt. Earn settlement.
- HUD `CLOSE · THE CONVERGE RULE`. Final fold locks into four words: `SEQUENCE · BIND · PROVE ·
  SETTLE`. Closing tokens: `CHECK_CONSENSUS=OK → TIER=1 → CHECK_RUNTIME_CONTRACT=PASS →
  TASK_LOOP=LOCAL_SETTLED|SETTLED → ACCEPTED=1`. "Make every transition inspectable, every authority
  singular, every loop finite, and every gap explicit."
- Final refusal: "Converge can prove conformity to an encoded contract. It cannot prove the original
  business decision was wise." Exit line: "The referee never scores its own goal."
- Sources [A] authority/operating docs; [D] trust docs; [T] composed demo.

---

## BACK MATTER (P71–P83)

### P71 — The construction-ready visual library (index)
- src: §6. Render diagram A (authority without duplication — mermaid: Human, Seamwise, Task-Spec,
  Converge, Executor, Cockpit/Ask; H→S→C→T→C→X→T→C; C -. snapshot .-> O). Index cards: B descent
  with bypasses → P14; C compose state machine → P26; D binding fences → P38; E loop kernel → P48;
  F receipt chain → P54; G observation boundary → P61. Note: "Reference compositions rebuilt with
  designed components; raw Mermaid is never pasted when a designed diagram communicates better."

### P72 — Reference tables · product authority + evidence objects
- src: §7. Table 1 (5 rows): WorkHelm / Seamwise / Task-Spec / Converge / Cockpit-Ask — Owns vs
  Explicitly does not own (exact cells from brief). Table 2 (6 rows): Review record, Composition
  receipt, HMAC authorization, Runtime contract, Execution receipt, AcceptanceRecord — Proves vs
  Does not prove (exact cells).

### P73 — Reference tables · pass contracts + compose responsibilities
- src: §7. Pass contracts table (9 rows, reference density allowed): pass, input, output, closing
  gate (CHECK_BRD=PASS … TASK_LOOP=* then ACCEPTED=1). Compose-vs table (6 rows): Prepare / Review /
  Preview / Materialize / Authorize / Settle across Converge / Seamwise / Task-Spec / Human.

### P74 — Reference tables · terminal states + truth corridors
- src: §7. Terminal states (8 rows with meaning, exit, work preserved — exact). Corridors (4 rows):
  immutable release v0.2.0/3de9f0b; committed main 58b1ddb / 57 forms; audited working tree
  58b1ddb + 16 modified + 1 untracked / 60 forms; future / no immutable revision (Manager/fleet and
  named non-promises as roadmap only).

### P75 — Reference table · verified and still open
- src: §7. 7 rows: composed single-task path ↔ no Manager/fleet scheduling; HMAC revision
  authorization ↔ shared-key identity/secrecy not proven; repository gate + postflight ↔ prevent
  class varies by adapter; optional different-family judge ↔ holdout not filesystem-separated; local
  settlement + independent acceptance ↔ production health not proven; Cockpit snapshot/Ask
  boundaries ↔ no operational write control by design; subsystem and extended gates ↔ aggregate
  make check red at layout.

### P76 — Code bank · the composed path + authorize/bind/run/accept
- src: §8. Two mac-window bash specimens: (1) export CVG_TASKSPEC_BIN, CVG_SEAMWISE_BIN; cvg compose
  prepare --source recipe.yaml / review --reviewer owner --reason "Topology and rollback accepted."
  / preview / materialize / status. (2) taskspec gate --stamp cvg/tasks/T-20260815-health-status.md;
  cvg bind --task …; cvg bind --check --task …; git add cvg/tasks cvg/execution; git commit -m
  "authorize and bind health status task"; cvg loop --issue T-20260815-health-status --agent codex.

### P77 — Code bank · machine contracts
- src: §8. Two mac-window JSON specimens: ConvergeCLIResult/v1 (exact fields incl.
  token COMPOSE=PREVIEW_READY, meta) and ConvergeCompositionReceipt/v1 (dispatch_authorized: false,
  source_commit, task_plan_digest, task_ids, task_digests).

### P78 — Code bank · policy + recovery + checkout-only
- src: §8. Three compact specimens: default-deny loop policy YAML (policy external_writes: deny;
  capabilities grants: []; budgets iterations 15, wall_seconds 5400, tokens 120000; isolation
  worktree). Recovery bash (cvg compose status --json; branch on token/exit_code/changed/dry_run;
  cvg loop --estimate / --gate-only; "Never convert BLOCKED/STALLED/EXHAUSTED into success.").
  Guided chat bash marked W: cvg next --guided --lane FULL; cvg next pre 5 --lane FULL; cvg next post 5.

### P79 — Presenter routes + demo placement
- src: §9. Route table: Executive 01–08, 22, 29–30, 37, 47, 54, 59–60, 72–76 (25–30 min); Method
  01–36, 47, 54, 59–60, 75–76 (50–60 min); Engineering all 76 (95–120 min); Workshop all 76 + live
  specimens (150–180 min). Demo placement list (8 stops): after S08 cvg agent-context --json; after
  S22 decided objection log + mutate reviewed plan in disposable fixture; after S30 inspect unsigned
  leaf + receipt; after S46 cvg bind --check (Git unchanged); after S54 cvg loop --estimate; after
  S60 retained v0.2.0/live-codex receipt chain; after S67 Cockpit on disposable workspace (never
  sensitive customer evidence); before S74 exact LAYOUT=FAIL output, do not fix live.

### P80 — Audience checks + per-slide acceptance checklist
- src: §9 + §10. Five audience questions with expected answers (which artifact authorizes dispatch →
  Task-Spec HMAC seal; who accepts → Task-Spec POST gate; does Cockpit control → no, read-only;
  what LOCAL_SETTLED excludes → external publication/tracker mutation; current aggregate status →
  subsystem proof broad, make check red at layout). Checklist (10 items verbatim-condensed): one
  slide one authority decision; headline is a claim; visual stands without notes; every green names
  source + proof token; release/main/tree/future distinct; no receipt grants unowned authority; no
  dotted line looks like a write path; code fits 1366×768; mobile order preserves semantics;
  transition creates one question.

### P81 — Canonical source index
- src: §11. Two-column dense index with labels: [A] OPERATING.md, AGENTS.md, docs/concepts/authority.md;
  [D] docs/trust/index.md; [C] VERSION, package.json, .claude-plugin/, contracts/cli-command-matrix.json,
  converge-cli-result-v1.schema.json, converge-composition-receipt-v1.schema.json,
  ui/v3/workspace-snapshot.schema.json; [I] bin/cvg, bin/_cvg_compose.py, bin/cvg-classify-lane.py,
  bin/cvg-snapshot.py, skills/evidence-to-next-pass/, idea-to-brd/, brd-docs-to-tech-req/,
  tech-req-to-adrs/, reqs-to-swimlane-plans/, sketch-plans-adversarial-review/, task-specs-to-issues/,
  task-to-runtime-contract/, task-loop/, external Task-Spec 3.8.x; [D] descent.md, bind-and-loop.md,
  recovery.md; [I] apps/cockpit/, install.sh, templates/; [T] Makefile, test-compose.sh,
  test-clean-room-install-e2e.sh, test-loop-kernel.sh, run-tests.sh, test-register.sh,
  test-cvg-json-envelope.sh, test-cvg-json-matrix.py, test-repo-layout.sh, Cockpit suites;
  [R] v0.2.0 tag 3de9f0b5f83f1bb62475308317c58e53f851b0db, release.yml;
  [E] evidence/releases/v0.2.0/live-codex/, invalidated alpha corridors; [D] README release truth.

### P82 — The sixteen editorial rules
- src: §12. All 16 rules verbatim-condensed as numbered cards (factory coordinator/referee never
  autonomous reasoning engine; nine passes/two phases/one barrier with Capture optional + Register
  opt-in; keep topology acceptance / task authorization / runtime binding / execution / acceptance /
  observation visually separate; reviewed/materialized/green/settled/accepted never synonyms;
  LOCAL_SETTLED vs SETTLED usage; Task-Spec 3.8.x explicit; W · CHECKOUT ONLY marking; hosted
  statements reported/immutable; layout failure in main narrative; HMAC = tamper evidence; tier-2
  holdout secrecy incomplete; adapter prevent/detect as recorded; no Cockpit/Ask/tracker/cvg next
  writing canonical truth; never imply merge/portfolio choice/widened authority; preserve failure
  tokens + exit semantics; end with honest product promise).

### P83 — Colophon / back cover
- Converge icon + Settlement Fold lockup. "Built from brf-converge.md — the deep-dive presentation
  architecture. Product: Converge 0.2.0 · Task-Spec 3.8.x · Seamwise pairing 0.2.0. Source audited
  2026-08-26 at 58b1ddb; release anchor v0.2.0 → 3de9f0b." Final line: "Sequence authority. Bind the
  attempt. Earn settlement."
