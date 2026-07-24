# Operação Dark Factory — Master Content Document

> **Purpose.** The single source of content for crafting the workshop
> presentation. Structure and timings mirror
> `docs/workshop-run-of-show-v1.md` (Run of Show v2); this document adds
> the material each act draws from: beats, key lines, slide topics,
> assets, numbers, and sources.
>
> **Internal — do not publish with the OSS repo.**

---

## 1. Governing rules

1. **Main intent.** The workshop is a 360° tease of the Bootcamp. Show
   the factory from outside, running for real; never open the machine.
   Every act builds desire for the "how" — the Bootcamp is the only
   place that delivers it.
2. **Stage rule — name, never open.** Converge and Task-Spec are the
   named stars. On screen they appear as silhouettes: what enters, what
   exits, what they guarantee. Fog inside every box. Never spoken:
   Fork, HMAC, safe-to-delegate, the contents of the 8 passes.
3. **Honesty doctrine.** The loop converges to green evals, not to
   truth. Say the limits out loud — with a senior room, honesty is the
   conversion engine.
4. **Privacy on stage.** Evidence shown from the legacy run must be
   privacy-safe and allowlisted. Type 01 may show its approved safe
   transaction reference and derived controls; never PAN, CPF, or a raw
   row. Worker packets are internally reconciled but scenario-unscored;
   the independent acceptance harness binds canonical identities to
   expected outcomes.
5. **Project-state boundary.** The legacy oracle was live-verified on
   2026-07-24: 25 canonical outcomes (15 success, 10 quarantine), four
   exact-batch restart seams, one integrity quarantine, one forced
   oracle mismatch; terminal cache and recovery-journal state empty.
   The Dark Factory demonstrated at the workshop is new work on top of
   this proven baseline.

## 2. The storytelling spine

**The through-line question** (on screen from Act 2 to the end):

> "Who guarantees the new number matches the old one — cent by cent?"

**The twist.** When the answer arrives (Act 3B), it points the other
way: the legacy — the supposed source of truth — was the one that was
wrong. The factory indicted the oracle.

**The real-world echo** (Act 4): KurvPay's stalled types prove the same
doctrine with real money: *the golden is evidence, not truth.*

**Recurring motifs** (plant early, harvest late):
- *The cent.* Money is the unit of truth all night.
- *Green ≠ true.* Planted in Act 1, detonated at the Act 3B AHA,
  echoed in the Act 5 close.
- *Watching vs. mastering.* The emotional gap the offer resolves.
- *The room as first demo.* The scoring system of Act 0 is the theme
  in miniature.

**The autonomy curve of the night.** The room doesn't gain autonomy
step by step (that's the Semana/Bootcamp); it *witnesses* total
autonomy once, in Act 3, and leaves wanting to build it.

## 3. The act structure

| # | Act | Duration | Job in the story |
|---|-----|----------|------------------|
| 0 | The Scoring Mechanism | 15 min | Belonging — "the first agentic system tonight is the one that scored you" |
| 1 | Fundamentals (not-101) | 45 min | Vocabulary + autonomy ladder; only what makes Act 3 legible |
| 2 | NorthWind Pay | 40 min | Legacy, works-but-wrong risk, BRD read-along, frozen budget, the question |
| — | Break | 10 min | Question stays on screen |
| 3A | The Anatomy (ignition first) | 25 min | Fire the factory; teach the machine over live telemetry |
| 3B | Lights-Off Execution | 45 min | The run: golden-match, divergence, the AHA, loop closes |
| 4 | KurvPay — the receipts | 20 min | Real numbers + stalled-types scar story; monetization lands here |
| 5 | The Bridge | 30 min | The gap, Monday workflows, Factory Ladder offer, honest close |

Total 3h50 + 10 min slack.

---

## Act 0 — The Scoring Mechanism (15 min)

**Objective.** The room recognizes itself as selected, understands what
it will witness, and buys the honesty contract.

**Beats**
1. Live Supabase pull on screen: applicants vs. selected, the
   Shapiro-level distribution of the room.
2. The frame: "the first agentic system you see tonight is the one
   that scored you."
3. Celebrate the selected without humiliating the rest (the funnel
   repositions non-approved people; their colleagues are in the room).
4. The promise: a factory will migrate a legacy financial system by
   itself and catch an error that hid for years — nobody types code in
   the loop.
5. The honesty contract + brief agenda.

**Slide/screen topics**
- Live data screen (Supabase query result, styled)
- Applicant distribution chart (Shapiro levels)
- The promise, one sentence, huge type
- Agenda of the night (acts as chapters)

**Key lines**
- "You were scored by a system against a criterion. That is literally
  what you'll watch a factory do with money tonight."
- "We won't sell magic. We'll show what's real and say exactly where
  the limits are."

**Assets/sources.** Supabase scoring data (live); qualification-funnel
design in `docs/wrksp-secret-dark-factory-v1.pdf` §3–4.

**Gate.** The room knows what it will witness and bought the contract.

---

## Act 1 — Fundamentals, not-101 (45 min)

**Objective.** Give the room exactly the vocabulary that makes Act 3
legible — nothing more. Best practices appear later as live-run
callbacks, not slides.

**Beats**
1. **Three names, three questions.** The Agentic Loop — how does a
   running system work? Converge — how does it deliver a project?
   ASD — how do you build the machine itself? (First appearance of the
   stars: names only.)
2. **The five layers.** L1 Model (pure text function, stateless) ·
   L2 Harness (a normal program: owns the API key, the while-loop,
   permissions) · L3 Tools (schemas offered as text) · L4 Environment
   (filesystem, git, databases, CLIs) · L5 Referee (deterministic
   gates and evals; exit 0/1 decides — the model's opinion is never
   consulted). *The model thinks, the harness acts, the referee
   judges.*
3. **The hop map + the misconception.** The model never invokes
   anything — it asks (emits a request blob); the harness calls.
   The while-loop wraps the hops; the referee judges outside them.
4. **The misconception table** (senior-room hook):
   - "The model runs commands" → the harness runs them
   - "The model remembers our conversation" → the transcript is re-sent
     in full every call
   - "The model knows my tools" → schemas are injected into every
     prompt; remove them, knowledge gone
   - "An agent is a special model" → agent = model + while-loop + tools
   - "MCP is a protocol models speak" → the model just sees more tool
     schemas
   - "Autonomy means a smarter model" → autonomy = a scheduler replaces
     the trigger and a referee replaces judgment
5. **The autonomy ladder** (Shapiro L0→L5 on the NHTSA frame):
   L0 Manual · L1 delegated tasks · L2 pairing in flow (where 90% of
   "AI-native" devs live) · L3 you became a manager reviewing diffs
   (where almost everyone stalls — and feels worse) · L4 you became a
   PM (spec, plan, come back in 12h) · L5 the autonomous factory
   (specs in, validated software out; humans not needed in the middle).
6. Close on the destination: "The factory you're about to see is L5."
   Plant: **the loop converges to green evals, not to truth.**

**Slide/screen topics**
- Three names / three questions table
- Five-layer ladder diagram
- Hop map (chat → assemble → emit → execute → transcript → referee)
- Misconception table (belief vs. reality)
- Autonomy ladder L0–L5 with "you are here" marker at L2–L3
- "Tonight = L5" destination slide

**Key lines**
- "The model never invokes anything. It asks; the harness calls."
- "Eval is the ring that frees you — without it you never trust
  autonomy."
- "Most of the market is parked at L3, reviewing diffs, feeling it got
  worse."
- "The loop converges to green evals, not to truth."

**Assets/sources.** `docs/asd-agentic-loop-v1.0.html` (five layers,
hop map, misconceptions, two seats); Shapiro ladder in
`docs/boot-uc-northwind-pay-edp-oss-v2.pdf` p.17 and workshop PDF p.12.
Converge/Task-Spec silhouette source: `docs/cvg-aut-systems-spine-steps-v5.pdf`,
`docs/task-spec-v3.2.0.pdf` (updates to come — fold in on arrival).

**Gate.** The room has the vocabulary, knows where it stands, and L5 is
named as tonight's destination.

---

## Act 2 — NorthWind Pay (40 min)

**Objective.** The room understands the legacy, feels the
works-but-wrong risk, and holds the unanswered question.

**Beats — a descent into the mine**
1. **The company.** Transactions in; every cycle the core spits 30+
   raw file types onto SFTP — proprietary positional layouts, COBOL
   overpunch, PII in the clear.
2. **The machine nobody touches.** Raw SFTP → Java black box (reads
   raw, anonymizes, emits sanitized CSV) → ~300 PL/pgSQL procedures
   closing the day. Business rules trapped inside the procedures.
   Show a real raw file — let them feel the overpunch. (Respect the
   privacy allowlist: safe reference and derived controls only.)
3. **The real risk.** Not downtime — *working and being wrong*. One
   swapped offset, one inverted sign: plausible-but-wrong money that
   green tests miss and an audit finds three months later. The numbers
   are the table stakes of the business.
4. **The BRD read-along (interactive).** Present the business
   requirements document as an artifact; read it together, interrogate
   it. Plants "understand before you build" — the value the factory
   demonstrates an hour later.
5. **The frozen budget.** Board wants to migrate; quote: 12–18 months
   of a full team. It froze on the question nobody could answer —
   through-line goes on screen and stays.
6. **The design secret.** The answer isn't more people — it's a
   factory. And the elegant part: **the legacy, defects and all, is
   the oracle.** Every translation is validated against the past, cent
   by cent.

**Slide/screen topics**
- NorthWind Pay topology (SFTP → Java → SFTP → Postgres → recon team)
- A real raw file on screen (allowlisted fields)
- "Works-but-wrong" risk slide (the plausible-wrong cent)
- The BRD document itself (read-along artifact)
- The frozen budget + the question (through-line slide)
- "The legacy is the oracle" concept slide

**Key lines**
- "The real risk is not the system going down. It's the system working
  — and being wrong."
- "Every file is surgery; the patient is the day's closing numbers."
- "The legacy, with all its defects, is the oracle."

**Assets/sources.** Legacy topology and case framing:
`docs/boot-uc-northwind-pay-edp-oss-v2.pdf` (fig. 02) and bootcamp
landing page; repo reality: `README.md`, `plans/legacy.md`,
`contracts/`, and the consolidated legacy architecture in
`plans/legacy.md`. **BRD: to be drafted** (from contracts + plans —
longest-lead content item).

**Gate.** Legacy understood, risk felt, question held.

---

## Break (10 min) — the question stays on screen

---

## Act 3A — The Anatomy, ignition first (25 min)

**Objective.** The room understands the machine that is — at that very
moment — visibly working behind the speaker.

**The pattern: ignite, then explain over a running machine.**

**Beats**
1. **Ignition (~3 min, ceremonial).** One visible chat invocation
   fires the factory on the chosen type. From this moment nobody
   touches the keyboard in the loop. Said out loud: *"While I explain
   how this works, it is working."*
2. **Live telemetry as backdrop.** Second screen: Linear cards moving
   column to column, branches appearing, a PR opening. Planned
   check-ins every few minutes ("look — it just passed the parser
   gate") stitch theory to evidence.
3. **The anatomy, silhouette-level:**
   - **What a Dark Factory is.** "Lights-out manufacturing" is the
     literal industry term: queue in, validated software out, humans
     not in the execution path.
   - **Chat invoking CLIs that do determinism** — the harness idea;
     the two seats (the CLI as a tool *inside* the loop; the CLI as
     launcher + referee *outside* it, never believing the
     self-report).
   - **Task-Spec** — the atomic unit: *"no eval, no task."*
   - **Converge** — the spine at 360°: pass names, inputs, outputs,
     fog inside every box. "What happens inside each pass is five
     nights of engineering." (The tease, delivered as fact.)

**Slide/screen topics**
- The ignition command (big, single, ceremonial)
- Split-screen layout: slides + live Linear/PR telemetry
- "Lights-out factory" concept slide (Fanuc reference)
- Two-seats diagram (CLI inside vs. outside the loop)
- Task-Spec silhouette card ("no eval, no task")
- Converge spine silhouette (names + fog)

**Key lines**
- "While I explain how this works, it is working."
- "The launcher never believes the thinker. It checks the world."
- "No eval, no task."
- "What happens inside each pass is five nights of engineering."

**Assets/sources.** ASD deck (two seats, launcher receipt); Converge
spine silhouette from `docs/cvg-aut-systems-spine-steps-v5.pdf`;
Task-Spec anatomy (silhouette only) from `docs/task-spec-v3.2.0.pdf`.

**Gate.** The machine is understood while visibly working.

---

## Act 3B — Lights-Off Execution (45 min) — THE HEART

**Objective.** The room witnesses the factory migrate, validate, and
indict the oracle — no human in the loop. L5 stops being a concept.

**Scope discipline.** 1 file type · 1 seam (transform) · 1 oracle ·
4 layers (model → parser → schema → writer) · 0 lines typed by hand.

**Beats**
1. **Walk the trail it already left.** Task-spec picked up, plan
   drafted, cross-provider adversary refuted the plan — show the
   objections and what changed. Cross-model disagreement is the point
   (anti-sycophancy, visceral for seniors).
2. **Watch the gates pass.** Narrate altitude, not code. "Green means
   the referee said so — not the model."
3. **Golden-match, live.** New output vs. legacy Postgres — the
   oracle — cent by cent, side by side.
4. **The divergence.** Numbers don't match. Room's instinct: "the new
   code has a bug." Let it breathe. Investigate on screen.
5. **The inversion — the AHA.** It's the *legacy* — a silent defect
   summing wrong cents for years. It always "worked." The factory
   indicted the oracle.
6. **The loop closes.** RED fed back; GREEN opened the PR. Migration
   validated — and the supposed source of truth proven wrong.

**Key line — said aloud at the AHA**
> "A wrong money number passes unnoticed — that is exactly why the
> golden-match exists. Eval engineering is not optional in a financial
> system."

**Demo type decision.** Type 05 recommended (HALF_UP rounding defect —
most explainable silent money error; file readable on a projector).
Alternative: Type 01 inverted overpunch (COBOL drama, harder to read).
Decide once; rehearse only that one.

**Production notes**
- Run duration must not depend on talking pace: pre-time stages; early
  finish → the PR waits; late → checkpoint recovery covers.
- Failure protocol: checkpoint worktree just before the reveal + cued
  backup recording. Errors on screen are fine; a stall is not.
- Rehearse second-screen choreography (Linear + PR view) as
  deliberately as the slides.

**Slide/screen topics**
- (Mostly live screens) adversary objections view; golden-match
  side-by-side; the divergence zoom; the indictment evidence; the PR.

**Assets/sources.** The live harness + repo; planted-defect design
(open item); golden-match comparator (to build); backup recording.

**Gate.** Witnessed: migrate, validate, indict. L5 became a thing seen.

---

## Act 4 — KurvPay: the receipts (20 min)

**Objective.** The room believes the pattern is real beyond the stage —
and sees what it is worth in money. (Monetization lands here, grounded
in measured numbers, not projections.)

**Beats**
1. **The reveal.** "What you just watched is not a demo trick.
   NorthWind Pay is the didactic, open-source twin of a real
   production engagement."
2. **The numbers** (see Numbers Bank): 29/32 types · 42s → 1s per
   file · 11.6h → 2s per thousand files · ~$2,500 → ~$25/month ·
   2–3 months per type by hand → ~8h agentic · golden-match signed
   against the original system, real money in the loop.
3. **The scar story — the real oracle indictment.** Two types stalled
   because the *golden itself* was defective (goldens exported from a
   different day / different year), proven from the golden's own
   header rows — and kicked back to the client rather than faked
   green. Doctrine: **"the golden is evidence, not truth."** The
   discipline the room just watched holds even when inconvenient.
4. **The frame.** "The demo was the trailer. This is the poster from a
   theater where it already played."

**Slide/screen topics**
- The reveal slide (NorthWind ↔ KurvPay twin)
- Numbers table (before/after, measured)
- Stalled-types scar story (the golden's own header as evidence)
- "The golden is evidence, not truth" doctrine slide

**Assets/sources.** `docs/kurv-edp-v2.pdf` (numbers, stalled types,
flywheel lessons).

**Gate.** Real beyond the stage; worth known in money.

---

## Act 5 — The Bridge (30 min)

**Objective.** The room feels the gap between watching and mastering —
and receives the Factory Ladder as the path, at the peak of intention.

**Beats**
1. **The honest bridge.** "You watched the factory run. What you did
   NOT see is how each piece was built — inside Converge, inside the
   task-specs, the harness, the referee, the fleet. That is not
   unlockable by watching. That is the Bootcamp."
2. **The ruler, one last time.** "Most of you live at L3. You just
   watched L5. The distance is engineering — and it's teachable."
3. **Your Monday (10 min max).** Generosity beat: 2–3 daily
   productivity workflows applicable immediately. Short, concrete, no
   internals. (Content to be selected — open item.)
4. **The Factory Ladder (offer).** Bootcamp pre-sale: Semana included,
   price locked before any public lot, credit flowing to Formação.
   Price ladder visible; credit rule explicit — 100%, no fine print.
5. **Close on honesty, not urgency.** "We showed what's real and where
   the limits are. The Bootcamp is where you build it with your own
   hands."

**Slide/screen topics**
- The bridge slide (seen vs. not-seen columns)
- Ladder recap with the L3→L5 gap highlighted
- Monday workflows (2–3 cards)
- The Factory Ladder offer screen (price ladder + credit rule)
- Honest close slide

**Assets/sources.** Offer mechanics: `docs/wrksp-secret-dark-factory-v1.pdf`
§13–14 (Escada da Fábrica, credit-that-flows, bundle logic).

**Gate.** Gap felt; ladder received at peak intention.

---

## 4. Numbers Bank

**KurvPay (real engagement — Act 4)**
- 29/32 file types migrated (didactic docs also cite 26/28
  golden-signed at an earlier cut — use 29/32 as current)
- Per-file processing: 42s → 1s (~42×)
- 1,000 files: 11.6h → 2s
- Infra cost: ~$2,500/month → ~$25/month (~98% reduction)
- Per-type effort: 2–3 months by hand → ~8h agentic
- 2 types stalled honestly: defective goldens, kicked back to client
- Flywheel: ~55–60 lessons distilled → 4 permanent skills
  (money, overpunch, positional, reconciliation)

**The legacy case (didactic — Act 2)**
- 30+ raw file types on SFTP
- ~300 PL/pgSQL stored procedures
- 12–18 months / 8–12 devs — the frozen migration quote
- 4–6 people reconciling numbers by hand at close

**The repo baseline (do not overclaim on stage)**
- 5 types implemented (01–05), migrations 001–010
- Oracle proof 2026-07-24: 25 canonical outcomes (15 success,
  10 quarantine), 4 restart seams, 1 integrity quarantine, 1 forced
  oracle mismatch

**The funnel (Act 0 context, internal)**
- ~50–60% target approval rate; 2 waves
- 12.2% of low-ticket buyers historically migrate to high ticket

## 5. Quote Bank (say these, verbatim)

1. "The first agentic system you see tonight is the one that scored
   you."
2. "The model never invokes anything. It asks; the harness calls."
3. "The loop converges to green evals, not to truth."
4. "The real risk is not the system going down. It's the system
   working — and being wrong."
5. "The legacy, with all its defects, is the oracle."
6. "While I explain how this works, it is working."
7. "The launcher never believes the thinker. It checks the world."
8. "No eval, no task."
9. "What happens inside each pass is five nights of engineering."
10. "A wrong money number passes unnoticed — that is exactly why the
    golden-match exists."
11. "The golden is evidence, not truth."
12. "You live at L3. You just watched L5. The distance is engineering
    — and it's teachable."

## 6. Source index

| Source | Feeds |
|---|---|
| `docs/workshop-run-of-show-v1.md` | The governing run of show (v2) |
| `docs/wrksp-secret-dark-factory-v1.pdf` | Funnel, scoring, moat discipline, offer mechanics (Acts 0, 5) |
| `docs/boot-uc-northwind-pay-edp-oss-v2.pdf` | Case framing, Shapiro ladder, bootcamp arc (Acts 1, 2, 5) |
| `docs/asd-agentic-loop-v1.0.html` | Five layers, hop map, misconceptions, two seats (Acts 1, 3A) |
| `docs/cvg-aut-systems-spine-steps-v5.pdf` | Converge silhouette (Act 3A) — updates pending |
| `docs/task-spec-v3.2.0.pdf` | Task-Spec silhouette (Act 3A) — updates pending |
| `docs/kurv-edp-v2.pdf` | Numbers, stalled types, flywheel (Act 4) |
| `README.md`, `plans/legacy.md`, `contracts/` | Legacy reality + BRD raw material (Act 2) |
| Past presentations (to be provided) | Slide raw material, all acts |

## 7. Open items

1. **Demo type decision** — Type 05 (recommended) vs Type 01.
2. **Planted legacy defect** — build for the chosen type, or accept
   fallback (live RED + KurvPay scar story carries the theme).
3. **Schedule conflict** — internal 19h30–23h30 vs public 09h00–13h00
   BRT. Resolve before publishing timings.
4. **Act 2 BRD** — to be drafted from contracts + plans.
5. **Monday workflows** — select the 2–3 to show in Act 5.
6. **Converge / Task-Spec updated docs** — fold into Act 3A silhouettes
   on arrival.
7. **Past presentations** — glue into acts on arrival.
