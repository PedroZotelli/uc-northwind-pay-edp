# 01 · The tour

**Minutes 4–14 · Claude Code, fresh session**

The agent explains your repository to the room. You do almost no talking.

---

## Paste this

```
This repository is new to me. Give me a guided tour.

Cover: what problem it solves, why there are two implementations of the same
thing, what each top-level folder is for, and the one rule the whole thing
rests on.

Read the READMEs rather than inferring from filenames. Show me the numbers —
lines per folder. Keep it to about two minutes of reading.
```

---

## What it does

Reads `README.md`, then the component guides. Comes back with the folder map, the
two-implementations argument, the four truth roles, and *no oracle, no build*.

## Why this card is first

**It proves the documentation is real.** Anyone can claim a repo is
self-documenting. Here an agent that has never seen it explains it correctly in
two minutes, from the READMEs, on the first try.

It also means the audience gets their orientation from the machine rather than
from you — which is a subtle signal that you are not selling them a tour you
rehearsed.

## What to point at while it reads

| | |
|---|---|
| `legacy/` — 29,732 lines | "The system that works. **Frozen.** Nothing may modify it to make a test pass." |
| `modern/` — 6,888 | "The same job, rebuilt independently. Twenty-three percent of the size." |
| `contracts/` — 5,748 | "**Neither of them is allowed to define what correct means.** This folder does." |

## The line to land

> "Two implementations that share no code, and one referee that outranks both.
> That is not academic — it is the only reason a mistake is *detectable* rather
> than merely absent from the logs."

## If it goes long

Cut in with: *"Skip to the one rule the whole repository rests on."* It will
answer **no oracle, no build**, which is where you wanted to be anyway.
