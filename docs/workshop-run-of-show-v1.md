# Operação Dark Factory — Run of Show v2 (internal)

> Internal stage document. Do not publish with the OSS repo.
>
> Stage rule v2 — **name, never open.** Converge and Task-Spec are the
> named stars of the night: they appear on screen, at 360°, as
> silhouettes (what enters, what exits, what they guarantee). What
> happens *inside* any pass is never shown — that is the Bootcamp.
> Deeper internals are still never said aloud: Fork, safe-to-delegate,
> HMAC, the contents of the 8 passes.
>
> Project-state boundary: the legacy oracle was live verified on 2026-07-24.
> Its automatic proof completed 25 canonical outcomes (`15` success, `10`
> quarantine), four exact-batch restart seams, one integrity quarantine, and
> one forced oracle mismatch; terminal cache and recovery-journal state was
> empty.
> The Dark Factory described below is a future workshop implementation and
> demonstration, not functionality already present in this legacy repository.

## The through-line

One question opens the night and never leaves the screen:

> **"Who guarantees the new number matches the old one — cent by cent?"**

Every act either sharpens that question or answers it. The twist: when
the answer arrives, it points the other way — the legacy, the supposed
source of truth, was the one that was wrong. The real-world echo
(KurvPay's stalled types) confirms it: **the golden is evidence, not
truth.**

## The acts — signed off

| # | Act | Duration | Job in the story |
|---|-----|----------|------------------|
| 0 | The Scoring Mechanism | 15 min | Belonging + "the first agentic system tonight is the one that scored you" |
| 1 | Fundamentals (not-101) | 45 min | Vocabulary + ruler; only what makes Act 3 legible |
| 2 | NorthWind Pay | 40 min | The legacy, the works-but-wrong risk, the BRD, the frozen budget, the question |
| — | Break | 10 min | Through-line question stays on screen |
| 3A | The Anatomy (ignition first) | 25 min | Fire the factory, then teach the machine over live telemetry |
| 3B | Lights-Off Execution | 45 min | Full attention on the run: golden-match, divergence, the AHA, loop closes |
| 4 | KurvPay — the receipts | 20 min | Real numbers + the stalled-types story; monetization lands here |
| 5 | The Bridge | 30 min | The gap, the Monday workflows, the Factory Ladder offer, honest close |

Total: 3h50 + 10 min slack.

## Act 0 — The Scoring Mechanism (15 min)

- Pull live approval data from Supabase on screen: applicants vs
  selected, the Shapiro-level distribution. A qualified room, not a
  generic audience.
- The frame that beats flattery: **"the first agentic system you see
  tonight is the one that scored you"** — a system evaluating against a
  criterion is literally the theme of the event.
- Celebrate the selected without humiliating the rest (the funnel
  repositions them; colleagues of people in the room didn't pass).
- The concrete promise + the honesty contract: "We won't sell magic.
  You'll watch a factory migrate a legacy financial system by itself —
  and we'll say exactly where the limits are."
- Brief agenda of the night.

**Gate:** the room knows what it will witness and bought the honesty
contract.

## Act 1 — Fundamentals, not-101 (45 min)

Discipline: teach only what makes Act 3 legible. "Best practices"
surface later as callbacks during the live run, not as slides here.

1. **The three names, three questions** (from the ASD deck): the
   Agentic Loop answers "how does a running system work?"; Converge
   answers "how does it deliver a project?"; ASD answers "how do you
   build the machine itself?" — first on-screen appearance of the
   stars, names only.
2. **The five layers**: model / harness / tools / environment /
   referee. The model thinks, the harness acts, the referee judges —
   only text and exit codes ever cross between them.
3. **The hop map + the misconception**: *the model never invokes
   anything — it asks; the harness calls.* The misconception table is
   the senior-room hook ("the model runs commands" → no it doesn't).
4. **The agent ladder / levels of autonomy** (Shapiro L0→L5 on the
   NHTSA frame). Place the room honestly: most of the market lives at
   L2–L3 and feels it got worse.
5. Close on the destination: "The factory you're about to see is L5."
   Plant the anti-hype seed that pays off twice later: **the loop
   converges to green evals, not to truth.**

**Gate:** the room has the vocabulary and knows where it stands, with
L5 named as tonight's destination.

## Act 2 — NorthWind Pay (40 min)

Descent into the mine:

1. **The company.** Transactions in, 30+ raw file types out onto SFTP
   every cycle: proprietary positional layouts, COBOL overpunch, PII in
   the clear.
2. **The machine nobody touches.** Raw SFTP → Java black box → ~300
   PL/pgSQL procedures that close the day. Business rules trapped
   inside. Show a real raw file — let them feel the overpunch.
3. **The real risk.** Not downtime — *working and being wrong*.
   Plausible-but-wrong money that green tests miss and audits find
   three months later. The numbers are table stakes of the business.
4. **The BRD read-along.** Present the business requirements document
   of the use case as an artifact; read it together, interrogate it.
   Plants "understand before you build" as a value the factory then
   demonstrates. (Interactive beat — the room talks.)
5. **The frozen budget.** 12–18 months of a full team; froze on the
   through-line question, on screen: *"Who guarantees the new number
   matches the old one, cent by cent?"*
6. **The design secret.** The answer isn't more people — it's a
   factory, and **the legacy, defects and all, is the oracle.**

Evidence shown from the legacy run must remain privacy-safe and allowlisted.
Type 01 may show its approved safe transaction reference and derived controls;
it must never show PAN, CPF, or a raw row. Worker packets are internally
reconciled but scenario-unscored; the independent acceptance harness is what
binds canonical identities to their expected outcomes.

**Gate:** the room understands the legacy, feels the works-but-wrong
risk, and holds the unanswered question.

## Break (10 min) — question stays on screen

## Act 3A — The Anatomy, ignition first (25 min)

**The pattern: ignite, then explain over a running machine.**

1. **Ignition (ceremonial, ~3 min).** One visible chat invocation fires
   the factory on the chosen type. From this moment, nobody touches the
   keyboard in the loop. Say it: "While I explain how this works, it is
   working."
2. **Teach the anatomy over live telemetry.** Second screen shows the
   factory's exhaust in real time: Linear cards moving column to
   column, branches appearing, a PR opening. Planned check-ins every
   few minutes ("look — it just passed the parser gate") stitch theory
   to evidence.
3. Content of the anatomy, all silhouette-level:
   - What a Dark Factory is (lights-out manufacturing — the industry
     term is literally "lights-out factory"): queue in, validated
     software out, humans not in the execution path.
   - Chat invoking CLIs that do determinism — the harness idea; the
     two seats (the CLI as a tool inside the loop; the CLI as
     launcher + referee outside it, never believing the self-report).
   - **Task-Spec**: the atomic unit — "no eval, no task."
   - **Converge**: the spine at 360° — pass names, what enters, what
     exits, fog inside every box. "What happens inside each pass is
     five nights of engineering." (The tease, delivered as fact.)

**Gate:** the room understands the machine that is, at this very
moment, visibly working behind the speaker.

## Act 3B — Lights-Off Execution (45 min) — THE HEART

Scope: **1 file type · 1 seam (transform) · 1 oracle · 4 layers
(model → parser → schema → writer) · 0 lines typed by hand.**

Full attention returns to the run:

1. **Walk the trail it already left.** Task-spec picked up, plan
   drafted, adversary (another provider) refuted the plan live —
   show the objections and what changed. Cross-model disagreement is
   the point, not noise.
2. **Watch the gates pass.** Narrate altitude, not code. Evals go
   green one by one — "green means the referee said so, not the
   model."
3. **Golden-match, live.** New output vs legacy Postgres — the oracle —
   cent by cent, side by side.
4. **The divergence.** Numbers don't match. The room's instinct: "the
   new code has a bug." Let it breathe. Investigate on screen.
5. **The inversion — the AHA.** It's the *legacy* — a silent defect
   summing wrong cents for years. It always "worked". The factory
   indicted the oracle.
6. **The loop closes.** RED fed back, GREEN opened the PR. Migration
   validated — and it proved the supposed source of truth wrong.

Said aloud at the AHA:

> **"A wrong money number passes unnoticed — that is exactly why the
> golden-match exists. Eval engineering is not optional in a financial
> system."**

**Demo type:** Type 05 recommended (HALF_UP rounding defect — the most
explainable silent money error; file readable on a projector).
Alternative: Type 01 inverted overpunch for COBOL drama. Decide once,
rehearse only that one.

**Production notes for the split-attention format:**
- The run's duration must not depend on talking pace: pre-time the
  factory's stages; if it finishes early, the PR waits; if late, the
  checkpoint recovery covers it.
- Failure protocol: checkpoint worktree just before the reveal +
  cued backup recording. Errors on screen are fine; a stall is not.
- Rehearse the second-screen choreography (Linear board + PR view)
  as deliberately as the slides.

**Gate:** the room witnessed the autonomous factory migrate, validate,
and indict the oracle. L5 stopped being a concept.

## Act 4 — KurvPay: the receipts (20 min)

Immediately after the AHA, energy hot. Monetization lands here,
grounded in measured numbers, not projections.

1. **The reveal.** "What you just watched is not a demo trick.
   NorthWind Pay is the didactic, open-source twin of a real
   production engagement."
2. **The numbers.** 29/32 file types · per-file processing 42s → 1s ·
   a thousand files 11.6h → 2s · ~$2,500 → ~$25/month · 2–3 months per
   type by hand → ~8h agentic · golden-match signed against the
   original system, with real money in the loop.
3. **The scar story — the real oracle indictment.** Two types stalled
   because the *golden itself* was defective (goldens exported from a
   different day / different year), proven from the golden's own
   header rows — and kicked back to the client rather than faked
   green. The doctrine line: **"the golden is evidence, not truth."**
   The discipline the room just watched holds even when inconvenient.
4. Frame: "The demo was the trailer. This is the poster from a theater
   where it already played."

**Gate:** the room believes the pattern is real beyond the stage — and
has seen what it is worth in money.

## Act 5 — The Bridge (30 min)

1. **The honest bridge.** "You watched the factory run. What you did
   NOT see is how each piece was built — inside Converge, inside the
   task-specs, the harness, the referee, the fleet. That is not
   unlockable by watching. That is the Bootcamp."
2. **The ruler, one last time.** "Most of you live at L3. You just
   watched L5. The distance is engineering — and it's teachable."
3. **Your Monday (10 min max).** The generosity beat: daily
   productivity workflows they can apply immediately — the "what
   changes Monday" route the FAQ promises. Short, concrete, no
   internals.
4. **The Factory Ladder (offer).** Bootcamp pre-sale: Semana included,
   price locked before any public lot, credit flowing to Formação.
   Price ladder visible; credit rule explicit (100%, no fine print).
5. **Close on honesty, not urgency.** "We showed what's real and where
   the limits are. The Bootcamp is where you build it with your own
   hands."

**Gate:** the room feels the gap between watching and mastering — and
receives the ladder as the path, at the peak of intention.

## Rehearsal checklist (before doors open)

- [x] Legacy clean-volume acceptance proof executed on 2026-07-24, with
      25 synchronous evidence packets and the separate automatic-worker gate
      passed. The worker proof covered `15` canonical successes, `10`
      canonical quarantines, four exact-batch restarts
      (`database_commit`, `raw_archive`, rejection `raw_quarantine`, and
      oracle mismatch), one integrity quarantine, and one oracle mismatch.
      It ended with 26 evidence packets and empty cache/journal state (the
      factory's oracle is proven before the show).
- [ ] Planted legacy defect implemented for the chosen demo type, with
      the independent business expectation preserved as evidence.
      NOTE: the repo's per-type scenario 5 is a *source-owned* control
      mismatch (legacy detects it) — the reveal needs the opposite: a
      silent defect *inside* the legacy path that the modern side
      catches. Fallback if it can't land in time: let golden-match
      catch a real RED live and close the loop; let KurvPay's
      stalled-types story carry the oracle-indictment theme.
- [ ] Full dress rehearsal of Acts 3A+3B with the real harness
      (orchestrator + adversary + executor) converging live, timed
      against the talk track.
- [ ] Second-screen choreography wired and rehearsed: Linear board +
      GitHub PR view visible while speaking.
- [ ] Backup recording of a successful run, cued and tested.
- [ ] Checkpoint worktree saved just before the reveal.
- [ ] Stage-language pass on every slide (name-never-open rule:
      Converge and Task-Spec at silhouette level only; Fork, HMAC,
      safe-to-delegate, pass internals never spoken).
- [ ] Act 2 BRD drafted, reviewed, and printed/on-screen ready.
- [ ] Offer screens final: price ladder + credit rule locked.
- [ ] Schedule confirmed: internal ementa says 19h30–23h30; public page
      says 09h00–13h00 BRT. Resolve before publishing timings.
