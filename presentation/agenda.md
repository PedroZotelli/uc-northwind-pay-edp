# Operação Dark Factory — Master Content & Run of Show

> **Purpose.** The single source of truth for the workshop: the run of
> show (act order, durations, gates) *and* the content each act draws
> from (beats, key lines, slide topics, assets, numbers, sources).
>
> **Internal — do not publish with the OSS repo.**
>
> **Supersedes** `docs/workshop-run-of-show-v1.md` (Run of Show v2) and
> `docs/content.md` (the standalone master content document), which were
> merged into this file. The operator cheat-sheet
> [`demo-script.md`](demo-script.md)
> stays separate: it holds the verified commands and their real output
> for Acts 3A/3B. This document is the narrative; that one is the
> keyboard.
>
> Lives beside the deck it feeds: `presentation/tmpl-agentic-engineering.html`
> and `presentation/images/`.

---

## 0. Latest state — read before touching any slide

**The Act 3B reveal changed on 2026-07-25.** Every earlier draft scripted
the AHA as *"it's the legacy — a silent defect summing wrong cents for
years; the factory indicted the oracle."*

**That is not what this system found.** The golden-match closed with
**zero** `CONFIRMED_LEGACY_DEFECT`. The legacy baseline is correct on all
five types. What exists is five **source-system** defects — the upstream
declared a total that its own detail rows contradict:

| Batch | Type | Source declared | Independently computed |
|---|---|---|---|
| `B202607230000004` | `01` | `173.44` | `173.45` |
| `B202607230000105` | `02` | `173.44` | `173.45` |
| `B202607230000205` | `03` | `198.49` | `198.50` |
| `B202607230000305` | `04` | `999.99` | `1000.00` |
| `B202607230000405` | `05` | `0.99` (fee) | `1.00` |

Delivering the old line would claim a defect the evidence does not
support, in front of an audience who may later read the repo. The true
reveal is stronger: the audience watches the machine **refuse to
conclude** when you take its evidence away.

**The AHA, said aloud:**

> "Three independent implementations — Java, SQL, and Python — each
> computed `173.45`. The source declared `173.44`. **Nobody corrected
> it.** Every system preserved the lie exactly as written, refused the
> batch, and kept the other batches running. The one cent never reached
> the database. And the factory can prove *who* lied, without ever
> showing you a card number."

**Consequences that ripple through this document**
- The Act 3B beats are rewritten (see Act 3B below).
- The "planted legacy defect" rehearsal item is **closed as
  not-needed** — the real finding replaced it.
- The demo type question is **settled**: Type 01, batch
  `B202607230000004`, for the beat-by-beat; all five types at the close.
- Act 4's KurvPay scar story is unaffected and still true — there, the
  *golden itself* was defective. The doctrine line **"the golden is
  evidence, not truth"** survives both stories.

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
4. **Claim discipline (hard limits).** Do not say, in any act:
   - "the factory found a legacy defect" — it did not; there are zero;
   - "the agent wrote all this unsupervised with no corrections" — the
     run was autonomous, but it found and fixed four vacuous gates
     along the way, which is the better story anyway;
   - "production-ready" or "CI-ready" — `plans/modern.md` forbids
     claiming either from local proof, and no CI exists;
   - "modern replaces legacy" — legacy is the frozen oracle; modern is
     an independent second implementation whose whole purpose is to
     disagree detectably.
5. **Privacy on stage.** Evidence shown from the legacy run must be
   privacy-safe and allowlisted. Type 01 may show its approved safe
   transaction reference and derived controls; never PAN, CPF, or a raw
   row. Worker packets are internally reconciled but scenario-unscored;
   the independent acceptance harness binds canonical identities to
   expected outcomes.
6. **Project-state boundary.** The legacy oracle was live-verified on
   2026-07-24: 25 canonical outcomes (15 success, 10 quarantine), four
   exact-batch restart seams, one integrity quarantine, and one forced
   oracle mismatch; terminal cache and recovery-journal state empty.
   The Dark Factory demonstrated at the workshop is new work on top of
   this proven baseline.

## 2. The storytelling spine

**The through-line question** (on screen from Act 2 to the end):

> "Who guarantees the new number matches the old one — cent by cent?"

**The twist.** When the answer arrives (Act 3B), it points somewhere
nobody expected: neither implementation was wrong. **The upstream source
lied by one cent** — and not one of the three systems silently corrected
it. They preserved the lie, refused the batch, and named the liar.

**The real-world echo** (Act 4): KurvPay's stalled types prove the same
doctrine with real money — there the *golden* was the defective party.
Same lesson from the other direction: *the golden is evidence, not
truth.*

**Recurring motifs** (plant early, harvest late):
- *The cent.* Money is the unit of truth all night.
- *Green ≠ true.* Planted in Act 1, detonated at the Act 3B AHA,
  echoed in the Act 5 close.
- *Refusing to conclude.* A system that declines beats a system that
  guesses with a confidence score.
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
   Shapiro-level distribution of the room. A qualified room, not a
   generic audience.
2. The frame that beats flattery: "the first agentic system you see
   tonight is the one that scored you" — a system evaluating against a
   criterion is literally the theme of the event.
3. Celebrate the selected without humiliating the rest (the funnel
   repositions non-approved people; their colleagues are in the room).
4. The promise: a factory will migrate a legacy financial system by
   itself and catch a money error that hid in plain sight — nobody
   types code in the loop.
5. The honesty contract + brief agenda of the night.

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
   judges* — only text and exit codes ever cross between them.
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
   Place the room honestly: most of the market lives at L2–L3.
6. Close on the destination: "The factory you're about to see is L5."
   Plant the anti-hype seed that pays off twice later: **the loop
   converges to green evals, not to truth.**

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
Converge/Task-Spec silhouette source:
`docs/cvg-aut-systems-spine-steps-v5.pdf`, `docs/task-spec-v3.2.0.pdf`
(updates to come — fold in on arrival).

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
   demonstrates an hour later. (The room talks here.)
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
Task-Spec anatomy (silhouette only) from `docs/task-spec-v3.2.0.pdf`;
pre-flight commands in `presentation/demo-script.md`.

**Gate.** The machine is understood while visibly working.

---

## Act 3B — Lights-Off Execution (45 min) — THE HEART

**Objective.** The room witnesses the factory migrate, validate, and
*name the liar* — no human in the loop. L5 stops being a concept.

**Scope discipline.** 1 file type · 1 seam (transform) · 1 oracle ·
4 layers (model → parser → schema → writer) · 0 lines typed by hand.

**Demo target — settled.** Type `01`, batch `B202607230000004`. One
cent, two detail rows. All five types at the close.

**Beats.** ~18 min of the 45 is the seven-beat terminal sequence; the
rest is the trail-walk, the gates, and the AHA breathing room. Exact
commands and their verified output live in
[`demo-script.md`](demo-script.md) —
keep it on the second screen.

1. **Walk the trail it already left.** Task-spec picked up, plan
   drafted, cross-provider adversary refuted the plan — show the
   objections and what changed. Cross-model disagreement is the point
   (anti-sycophancy, visceral for seniors).
2. **Watch the gates pass.** Narrate altitude, not code. "Green means
   the referee said so — not the model."
3. **The lie, in the source's own words.** The source manifest declares
   `net_amount: 173.44`. *"Hold that number."*
4. **Three independent implementations, one answer.** Legacy Java
   parser, read-only PostgreSQL SQL, modern Python parser — all three
   computed `173.45`; all three kept the source's `173.44` exactly as
   written. *"Three implementations that share no code. Nobody rounded
   it away, nobody 'helpfully' corrected it."*
5. **The divergence, then containment.** Numbers don't match. Room's
   instinct: "the new code has a bug." Let it breathe. Then: staging
   rows `0`, business rows `0`, status `quarantined`. *"Not rolled
   back — never written. The cent never entered the database."*
   And the blast radius is one batch: the two batches after it
   succeeded and reconciled.
6. **Run the detector live — the attribution.** Point at four things
   only, never read JSON aloud: `attribution.owner:
   "source_system_of_record"` (**who**); `attribution.basis[]` — three
   named rules with the channels that fed each (*"the explanation is a
   list a test can check, not a sentence a model wrote"*);
   `controls.compared[]` — `detail_count` matches, `net_amount` does
   not; `observations[].independence` — each channel labelled.
   *"No card number. No document. No raw row. Nothing in here you
   wouldn't put in a ticket."*
7. **Take its evidence away — the money shot.** Withhold any single
   channel and the detector returns `DF-E-ATTRIBUTION-INCONCLUSIVE`.
   *"Remove any single piece of evidence and it refuses to conclude.
   It does not lower a confidence score — it declines. That is the
   difference between a system that reasons from evidence and one that
   produces opinions."* Worth telling: the **first** version of this
   rule passed *every* withhold probe, because it asked for "at least
   two of three." The gate was green and proved nothing. The run
   caught it and tightened it.
8. **Determinism.** Run the detector twice; identical `finding_id`
   hash. *"Byte-identical on four runtimes built from scratch on
   different days. The finding is a fact, not a generation."*
9. **Close the loop — all five types.** Five lines, five types, five
   source defects, **zero unexplained differences.** COBOL overpunch,
   escaped pipes, 240-byte paired segments, heterogeneous widths,
   semicolon CSV with decimal commas — every difference classified.

**Key line — said aloud at the AHA**
> "Three independent implementations each computed 173.45. The source
> declared 173.44. Nobody corrected it. Every system preserved the lie
> exactly as written, refused the batch, and kept the other batches
> running. The one cent never reached the database — and the factory
> can prove *who* lied, without ever showing you a card number."

Then the doctrine callback:

> "A wrong money number passes unnoticed — that is exactly why the
> golden-match exists. Eval engineering is not optional in a financial
> system."

**Optional +5 min — the honest engineering beat.** Lands hard with
senior engineers and is entirely true. Four gates in this build passed
while proving nothing, and the run caught each:
1. The withhold probe was unfalsifiable (beat 7).
2. `make check` served the Java suite from a **build cache** — 78 tests
   "passed" without executing on the committed bytes.
3. Golden-match reported **legacy parity while never contacting
   legacy** — a missing driver plus a bare `except` degraded it to
   contract-only comparison.
4. The Type 04 account token hashed the account number alone where the
   contract says `ispb:branch:account`. Tokens were well-formed,
   deterministic, stable — every structural test passed. Only
   byte-for-byte comparison against the approved output caught it.
   That bug would have made the same account at two different banks
   share a token.

> "Every one of those was green. Green is not the goal — **green for
> the right reason** is. That is what eval engineering buys you."

**Production notes**
- Run duration must not depend on talking pace: pre-time stages; early
  finish → the PR waits; late → checkpoint recovery covers.
- Terminal: 16pt minimum, dark background, ~100 columns. Nothing in
  the demo script needs more width.
- Failure protocol: checkpoint worktree just before the reveal + cued
  backup recording. Errors on screen are fine and on-brand; a stall is
  not. Fall back to reading the committed evidence packets under
  `evidence/factory/` and `evidence/modern/` — they are already on
  disk from the pre-flight.
- Rehearse second-screen choreography (Linear + PR view) as
  deliberately as the slides.

**Slide/screen topics**
- (Mostly live screens) adversary objections view; the source manifest;
  the three-implementation comparison; the containment query; the
  detector output; the withhold sweep; the twin hashes; the five-type
  close; the PR.

**Assets/sources.** The live harness + repo;
`presentation/demo-script.md` (verified commands and output);
`.runtime/e2e-evidence/`, `evidence/modern/`, `evidence/factory/`;
backup recording.

**Gate.** Witnessed: migrate, validate, attribute — and refuse to
conclude without evidence. L5 became a thing seen.

---

## Act 4 — KurvPay: the receipts (20 min)

**Objective.** The room believes the pattern is real beyond the stage —
and sees what it is worth in money. (Monetization lands here, grounded
in measured numbers, not projections. Play it immediately after the
AHA, energy hot.)

**Beats**
1. **The reveal.** "What you just watched is not a demo trick.
   NorthWind Pay is the didactic, open-source twin of a real
   production engagement."
2. **The numbers** (see Numbers Bank): 29/32 types · 42s → 1s per
   file · 11.6h → 2s per thousand files · ~$2,500 → ~$25/month ·
   2–3 months per type by hand → ~8h agentic · golden-match signed
   against the original system, real money in the loop.
3. **The scar story — the same discipline, the other direction.** Two
   types stalled because the *golden itself* was defective (goldens
   exported from a different day / different year), proven from the
   golden's own header rows — and kicked back to the client rather
   than faked green. Doctrine: **"the golden is evidence, not
   truth."** On stage tonight the source lied; on that engagement the
   golden lied. The discipline holds either way, even when
   inconvenient.
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
   productivity workflows applicable immediately — the "what changes
   Monday" route the FAQ promises. Short, concrete, no internals.
   (Content to be selected — open item.)
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

**Assets/sources.** Offer mechanics:
`docs/wrksp-secret-dark-factory-v1.pdf` §13–14 (Escada da Fábrica,
credit-that-flows, bundle logic).

**Gate.** Gap felt; ladder received at peak intention.

---

## 4. Rehearsal checklist (before doors open)

- [x] **Legacy clean-volume acceptance proof** executed on 2026-07-24,
      with 25 synchronous evidence packets and the separate
      automatic-worker gate passed. The worker proof covered `15`
      canonical successes, `10` canonical quarantines, four exact-batch
      restarts (`database_commit`, `raw_archive`, rejection
      `raw_quarantine`, and oracle mismatch), one integrity quarantine,
      and one oracle mismatch. It ended with 26 evidence packets and
      empty cache/journal state — the factory's oracle is proven before
      the show.
- [x] **Act 3B reveal corrected** to the source-system finding, with
      the commands and output verified against this checkout
      (2026-07-25). The "planted legacy defect" item is closed as
      not-needed: the real finding is stronger than the planted one.
- [x] **Demo target locked:** Type `01`, batch `B202607230000004`, plus
      the five-type close.
- [ ] **Pre-flight run** on the show machine:
      `make clean CONFIRM=clean-runtime` → `make deploy` (~30s) →
      `make test-e2e TYPE=all` (~3 min) → `make df-accept TYPE=all`
      (~30s). Fixture keys exported in the demo shell (see the demo
      script's `export` block; they live in `.env`).
- [ ] **Full dress rehearsal of Acts 3A+3B** with the real harness
      (orchestrator + adversary + executor) converging live, timed
      against the talk track.
- [ ] **Second-screen choreography** wired and rehearsed: Linear board
      + GitHub PR view visible while speaking; terminal at 16pt, dark,
      ~100 columns.
- [ ] **Backup recording** of a successful run, cued and tested.
- [ ] **Checkpoint worktree** saved just before the reveal.
- [ ] **Stage-language pass** on every slide (name-never-open rule:
      Converge and Task-Spec at silhouette level only; Fork, HMAC,
      safe-to-delegate, pass internals never spoken). Same pass must
      catch any surviving "legacy defect" phrasing — see §1.4.
- [ ] **Act 2 BRD** drafted, reviewed, and printed/on-screen ready.
- [ ] **Offer screens final:** price ladder + credit rule locked.
- [ ] **Schedule confirmed:** internal ementa says 19h30–23h30; public
      page says 09h00–13h00 BRT. Resolve before publishing timings.

## 5. Numbers Bank

**The live demo (verified 2026-07-25 — Act 3B)**
- 5 source-system defects, one per type; **zero** confirmed legacy
  defects; **zero** unexplained differences
- Demo batch `B202607230000004`: declared `173.44`, computed `173.45`
  by three independent implementations (Java, SQL, Python)
- Containment: staging rows `0`, business rows `0`, status
  `quarantined`; adjacent batches succeeded
- Withhold sweep: 4 of 4 channels → `DF-E-ATTRIBUTION-INCONCLUSIVE`
- Determinism: identical `finding_id` across runs and across four
  runtimes built from scratch on different days
- 4 vacuous gates found and fixed by the run itself (unfalsifiable
  withhold probe; cached Java suite; golden-match never contacting
  legacy; Type 04 token scope)

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
- No CI exists; nothing here is production-ready or CI-ready

**The funnel (Act 0 context, internal)**
- ~50–60% target approval rate; 2 waves
- 12.2% of low-ticket buyers historically migrate to high ticket

## 6. Quote Bank (say these, verbatim)

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
10. "Three implementations that share no code. All three computed
    173.45. Nobody corrected the source."
11. "Not rolled back — never written. The cent never entered the
    database."
12. "Remove any single piece of evidence and it refuses to conclude.
    It does not lower a confidence score — it declines."
13. "A green gate that cannot fail is worse than a red one."
14. "Green is not the goal — green for the right reason is."
15. "The finding is a fact, not a generation."
16. "A wrong money number passes unnoticed — that is exactly why the
    golden-match exists."
17. "The golden is evidence, not truth."
18. "You live at L3. You just watched L5. The distance is engineering
    — and it's teachable."

## 7. Source index

| Source | Feeds |
|---|---|
| `presentation/demo-script.md` | Verified commands, real output, the corrected reveal (Acts 3A, 3B) |
| `docs/wrksp-secret-dark-factory-v1.pdf` | Funnel, scoring, moat discipline, offer mechanics (Acts 0, 5) |
| `docs/boot-uc-northwind-pay-edp-oss-v2.pdf` | Case framing, Shapiro ladder, bootcamp arc (Acts 1, 2, 5) |
| `docs/asd-agentic-loop-v1.0.html` | Five layers, hop map, misconceptions, two seats (Acts 1, 3A) |
| `docs/cvg-aut-systems-spine-steps-v5.pdf` | Converge silhouette (Act 3A) — updates pending |
| `docs/task-spec-v3.2.0.pdf` | Task-Spec silhouette (Act 3A) — updates pending |
| `docs/kurv-edp-v2.pdf` | Numbers, stalled types, flywheel (Act 4) |
| `README.md`, `plans/legacy.md`, `contracts/` | Legacy reality + BRD raw material (Act 2) |
| `plans/modern.md` | Claim limits — what may not be said on stage (§1.4) |
| Past presentations (to be provided) | Slide raw material, all acts |

## 8. Open items

1. **Act 2 BRD** — to be drafted from contracts + plans (longest lead).
2. **Monday workflows** — select the 2–3 to show in Act 5.
3. **Schedule conflict** — internal 19h30–23h30 vs public 09h00–13h00
   BRT. Resolve before publishing timings.
4. **Converge / Task-Spec updated docs** — fold into Act 3A silhouettes
   on arrival.
5. **Past presentations** — glue into acts on arrival.

*Closed:* demo type decision (Type 01 / `B202607230000004`, settled
2026-07-25); planted legacy defect (not needed — the real
source-system finding replaced it).
