# 09 · The cent

**Minutes 62–65 · close here**

This is the card the whole hour was built for. **Do not skip it, even if you are
over time.** Cut card 08 short instead.

---

## Paste this

```
One last thing. The source-defect batch.

Show me what the source declared, what your parser computed, and how golden-match
classified the difference. Then tell me what you did NOT do to that number.
```

---

## What the room sees

```
declared (source)      0.99
computed (modern)      1.00
classification         CONFIRMED_SOURCE_DEFECT
unexplained_count      0
status                 quarantined
```

---

## The close

> "The machine wrote that parser twenty minutes ago, from a specification, without
> reading anyone's implementation.
>
> The source said the fee was ninety-nine cents. Its own rows compute one real.
> **The parser found the cent.**
>
> And here is the part that matters: **it did not fix it.** It kept the source's
> `0.99` exactly as published, refused the batch, and named who lied. Because a
> system that silently repairs its input has destroyed the evidence that something
> upstream is broken."

Pause. Then:

> "That is the whole talk. Not that an agent can write code — you already knew
> that. **That an agent can be graded, by something it is not allowed to touch,
> on a number that matters.**
>
> Auto-allow is a bet on your gates. Go and try to break one of yours this week.
> If you cannot make it go red, it was never protecting you."

Stop there.

---

## Why the rounding is the real test

Worth thirty seconds if you have them:

> "Python's default rounding is banker's rounding — `ROUND_HALF_EVEN`. This
> contract mandates `HALF_UP`. `round()` and f-string formatting both quietly give
> you the wrong one.
>
> Every structural test would pass. The tokens would be well-formed, the row
> counts would match, the types would be right. **Only a byte-for-byte comparison
> against a human-approved file catches a one-cent rounding error.**
>
> That is the same shape as a bug this repository already found: an account token
> hashed the account number alone where the contract said bank plus branch plus
> account. Well-formed, deterministic, stable — and it would have given the same
> account at two different banks the same token."

---

## If the factory got the rounding wrong

**Lead with it. It is the better ending.**

> "It used HALF_EVEN. Ninety-nine cents against a real. The referee caught it, and
> then it fixed it.
>
> I could not have designed a better demonstration. **That one cent is the entire
> argument for building the same system twice.**"

---

## The one-liner, if you need to run it manually

```bash
python3 -c "
import json,glob
for p in sorted(glob.glob('evidence/modern/*/golden-match.json')):
    d=json.load(open(p))
    for x in d['differences']:
        print(f\"  {d['batch_id']}  {x['classification']:26} {x['field']:22} computed={x['modern']:>8}  declared={x['reference']:>8}\")"
```
