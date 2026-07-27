# 07 · The nudge

**Only if it drifts. Use once.**

---

## Paste this

```
Status. One line per gate: what is green, what is red, what you are doing next.
```

---

## Why it is this short

A long corrective prompt on stage looks like you steering, and steering
contradicts the entire claim you have just spent forty minutes making. Nine words
that ask for a status report do not.

## What good looks like

```
ingestion    green — parser + schema + writer written, 4 scenarios parse
dlt          green — registered, 3 rows in landing
dbt bronze   green
dbt silver   RED — assert_type05_silver_preserves_bronze_totals fails on fee column
next         reading the conservation macro, my Silver drops calculated_fee_brl
```

That is a system reasoning. Read it aloud — it is better material than a clean run.

## If it comes back vague

One more, and only one:

```
Which gate is red right now, and what is your next concrete action?
```

## If it is still circling after that

Stop. Do not paste a third time.

> "It is stuck. That is worth seeing too — let me show you what it produced and
> where it got to, and then we can talk about why."

Then card 08 on whatever it did produce, or card 09 on the committed evidence for
types 01–04.

**Three nudges in a row is you doing the work.** The audience will notice, and the
claim collapses. One nudge is a status check. That is the line.
