# 03 · Who lied, and prove it

**Minutes 24–34 · the strongest card before the invocation**

---

## Paste this

```
Batch B202607230000004 was refused. I want to know who is at fault, and I want
you to prove it rather than assert it.

Show me, in this order:
1. what the source declared, in its own words
2. what each independent implementation computed — Java, SQL, and Python
3. what reached the database
4. whether the batches around it survived
5. the detector's attribution, and the basis it rests on

Then run the withhold probe: re-run the detector four times, each time removing
one observation channel, and show me what it does.
```

---

## What the room sees

```
source declares: {"currency": "BRL", "detail_count": 2, "net_amount": "173.44"}

legacy Java parser   declared=173.44  computed=173.45
PostgreSQL read-only SQL           computed=173.45
modern Python parser declared=173.44  computed=173.45

staging rows=0 | business rows=0 | status=quarantined

B202402290000001 | succeeded
B202607230000002 | succeeded
B202607230000004 | quarantined

  withhold legacy-source-manifest           -> DF-E-ATTRIBUTION-INCONCLUSIVE
  withhold legacy-java-processor            -> DF-E-ATTRIBUTION-INCONCLUSIVE
  withhold legacy-postgres-control-plane    -> DF-E-ATTRIBUTION-INCONCLUSIVE
  withhold legacy-postgres-diagnostic       -> DF-E-ATTRIBUTION-INCONCLUSIVE
```

## The three lines

> "Java, SQL and Python. Three implementations that share no code. All three
> computed 173.45. All three kept the source's 173.44 **exactly as written** —
> nobody rounded it away, nobody helpfully corrected it. A system that silently
> fixes its input has destroyed the evidence that something upstream is broken."

> "Zero rows. Not rolled back — **never written.** The cent never entered the
> database. And one batch stopped while the two around it succeeded. A bad file
> does not take the night down."

> "Remove any single piece of evidence and it **refuses to conclude.** It does not
> lower a confidence score. It declines. That is the difference between a system
> that reasons from evidence and one that produces opinions."

## Then confess. Immediately.

**This is the highest-trust move in the hour. Do not save it for later.**

> "The first version of that probe passed with *any* channel removed, because the
> rule asked for 'at least two corroborations out of three.' The gate was green
> and proved nothing. The autonomous run caught it and tightened it."

## Why it belongs here

Everything after this card depends on the audience believing that green means
something in this repository. This is where you earn that — by showing a gate
that refuses, and then admitting the first version of it could not.
