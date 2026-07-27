# 06 · The invocation

**Minutes 44–46 · then you step back and talk for twelve minutes**

---

## First, turn on auto-allow. Out loud.

> "This is the checkbox. From here it does not ask me anything. Everything I have
> shown you for the last forty minutes is now the only thing standing between it
> and this repository."

---

## Then paste this

```
/fab translate spec/type-05-merchant-fee-assessment
```

**That is the whole prompt.**

---

## Say this immediately

> "Notice how little I typed. One command and a folder.
>
> **The policy is not in my prompt — it is in the repository and in the skill.**
> The frozen paths, the forbidden actions, the halt conditions, the definition of
> done. That is the difference between prompting an agent and running a factory."

That single observation is worth more than the next ten minutes of output.

---

## Fallback, if `/fab` did not register

Paste this instead. Same content, longer form:

```
Read .claude/skills/fab/SKILL.md and execute the `translate` verb against
spec/type-05-merchant-fee-assessment.

You are at autonomy level 5: do not ask me for approval, do not stop to confirm,
run to a pull request. Everything you need — the mandate, the frozen paths, the
forbidden actions, the halt conditions, the loop, and the definition of done —
is in that skill file and in the work order. Go.
```

---

## What is carried for you, not typed

| | |
|---|---|
| **L5 mandate** | never ask; gate-passing increments on `factory/type-05-modern` |
| **Frozen** | `legacy/` `contracts/` `gen/` `infra/` applied migrations |
| **Forbidden** | git archaeology for the deleted implementation — *and if you look, say you looked* |
| **Halt** | restricted value in output · write to a frozen path · gate unpassable without changing frozen truth |
| **The loop** | act → observe artifacts → gate on golden-match → repeat |
| **Done when** | golden-match resolves · zero unexplained · the cent classified · **and a PR is open** |

---

## What to say while it works

Do not watch silently. Twelve minutes is a lot of air.

| When you see | Say |
|---|---|
| It reads the specification | "It is reading the spec, not the Java. If it read the Java it would inherit its bugs and call that parity." |
| It writes `parser.py` | "Five files per type, same rhythm as the other four. It inferred that convention from the repository — I did not give it a template." |
| It writes dbt models | "Bronze, Silver, Gold — **and the type tag.** An untagged test silently never runs in a scoped build. That detail decides whether this works." |
| Something fails | **The best moment available to you.** "Watch. It is not asking me. It reads the error, forms a hypothesis, tries again." |
| golden-match runs | "Now the referee speaks. Not the agent." |

And this is your window for the material that does not need the screen:

- the **L1–L5 ladder**, and why L4 is the rung nobody else claims
- the **six gates that could not fail** — the build cache, the parity check that
  never contacted legacy, the token that would have collided across two banks
- **loop-readiness is falsifiable gates, not tooling**

---

## The rule for stalling

If it circles for more than about four minutes, use card 07 once.

If that does not move it: **say so plainly and cut to card 09.** The committed
evidence for types 01–04 is on disk and makes every point you need.

> "It is struggling. Let me show you what happens when it works, and then we can
> talk about why it did not."

An honest cut costs you nothing. A silent ten-minute stall costs you the room.
