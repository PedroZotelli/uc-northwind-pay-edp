# 05 · The arrival

**Minutes 40–44 · the SpecIngestor beat**

The requirement lands. The factory reads it and **builds nothing.**

---

## Paste this

```
A new file type landed in spec/ this morning. Read the pack.

Tell me: what has the customer asked for, what did they actually give us, what
is missing — and most importantly, is this specification adjudicatable?

Do not write any code yet.
```

---

## What it does

Reads `WORK-ORDER.md` and `INVENTORY.md`, walks the seven numbered folders, and
reports. **The "build nothing yet" instruction is the point of the card.**

## What it should come back with

| | |
|---|---|
| Received | the four contract YAMLs · 5 raw inputs · the sanitized outputs the Java produces · the approved reconciliations · two approved refusals · **one real legacy execution, 13 artifacts** · the shape of the deliverable |
| Missing | the modern vertical — ingestion, dbt, tests, wiring. ~1,000 lines |
| Adjudicatable? | **Yes.** Every scenario ships an approved expected output |

## The lines

> "Notice what is in this pack. A specification. Real inputs. The outputs the
> current system produces. One complete execution. **No code.** They did not send
> us a translation — because if they had, we would be porting, and the referee
> would be comparing a copy with its original."

> "About 5,800 lines of ground truth arrived. About a thousand is missing. **That
> thousand is the job, and the other 5,800 is what will grade it.**"

## The moment that matters

When it says *"yes, this is adjudicatable — every scenario ships an approved
output"* — stop and mark it:

> "That is the rule the whole repository rests on, and the machine just applied it
> without being asked. **No oracle, no build.** If this pack had arrived without
> expected outputs, the correct answer would have been to refuse it and write no
> code at all."

Every person in that room has shipped against a spec with no acceptance criteria.
This is the card where they feel it.

## Optional, and very cheap

```bash
diff spec/type-05-merchant-fee-assessment/02-raw-in/valid-minimal.csv \
     spec/type-05-merchant-fee-assessment/03-sanitized-out/valid-minimal.sanitized.csv
```

> "Raw in, sanitized out. Every transformation between those two files is written
> down in the specification. **None of it is discretionary.** That is why a second
> implementation is possible at all."
