# 05 · Query Second Brain — Java as concepts

- Slide: Board 2 · Grasp — Show, then J1–J5 (HUD not signed)
- Slice: **C · Grasp**
- Who: every seat, **their** notebook from Day 1. Do not rebuild
- Next: [`06-specs-graph.md`](06-specs-graph.md)

AI-native: you do not have to *know* Java. You have to grasp what the Java **plant does**. Ask the brain. Cite a page. Do not paste `legacy/processor/src`.

## Prompt (verbatim) — paste one, wait, then the next

**J1 — privacy boundary**

```text
From the sources in this notebook only:
What is a privacy boundary for Type 01 card settlement?
What must never leave sanitize (PAN, CPF)?
Cite the page. If it is not in the sources, say you do not have it.
```

**J2 — overpunch**

```text
What is signed overpunch? In these sources, what does 00000001234E mean?
What does the Type 01 trailer declare vs what the detail rows add to?
Cite Marina if she is in the sources. Do not invent Java.
```

**J3 — refuse vs crash**

```text
What does “refuse the batch” mean for a source lie?
Is a refusal a crash? What must the new plant not do to the trailer?
Cite a source.
```

**J4 — sanitize, in one paragraph**

```text
In one paragraph: what does the legacy plant do when it sanitizes Type 01?
Use inbound language (layout, tokenize, last4). Do not quote a .java file. Cite the page.
```

**J5 — what is not here**

```text
Do these sources contain the Java parser? If I need legacy/processor/src to answer, say you do not have it.
```

## Proof

J2 cites Marina: **173.44** vs **173.45**. J1 names PAN / CPF. J5 does **not** invent Java source. No file in git was written. Notebook still has **nine** sources. Do not Add sources tonight.

## If fail

No Google / empty notebook → pair with a neighbour. They still have `spec/` on disk. Do not dump Java into NotebookLM to “fix” it.
