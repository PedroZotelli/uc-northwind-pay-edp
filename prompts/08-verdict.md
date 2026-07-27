# 08 · The verdict

**Minutes 58–62 · the referee speaks, not the agent**

---

## Paste this

```
Summarise for an audience who has been watching.

What did you build, roughly how many lines, and how do you know it is correct?

Quote the referee — golden-match — not your own test run. Then show me the pull
request, and tell me anything you had to work out along the way.
```

---

## The distinction this card exists to make

**An agent saying "tests pass" is a claim. An independent oracle saying
"byte-identical to the human-approved answer" is evidence.**

You have spent an hour building the audience's ability to feel that difference.
This is where you cash it. So when it answers, do not let it summarise — make it
quote:

```json
{ "batch_id": "B202607230000401", "outcome_class": "accepted",
  "resolved": true, "unexplained_count": 0, "differences": [] }
```

> "That is not the agent's opinion of its own work. That is a comparison against
> files it was forbidden to touch, written by a human before it started."

---

## The pull request

Whatever else happens, this is the artifact to end on. It should carry: what was
built, the referee's verdict, the defect classification, and what it had to work
out.

> "A work order went in. A pull request came out, with the evidence attached.
> **Nobody approved a step.** And the thing at the end is not a promise that it
> works — it is a comparison a human can check in thirty seconds."

---

## If it built it clean

Do not oversell. Say the honest thing:

> "That was cleaner than I expected. Which means either the specification was
> good — or something is not being tested. Both of those are worth knowing, and
> the only reason I can tell the difference is the referee."

## If the referee caught it out

**Better card.** Lead with it:

> "Look at that. It built something plausible, and an oracle it could not touch
> said no. Then it fixed it. **That is the loop** — and it is the only version of
> autonomy I would run against a payment system."

---

## What not to let it claim

If it says *deployed*, *production-ready*, or *CI-ready* — correct it on the spot.
There is no deployment target and `plans/modern.md` forbids the claim.

> "It did not deploy. It ran until every gate closed and the referee signed off.
> **Deployment is a decision a human makes with that evidence in hand.**"
