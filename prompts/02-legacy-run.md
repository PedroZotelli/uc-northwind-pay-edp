# 02 · One batch, end to end

**Minutes 14–24**

Stop talking about the brownfield. Run it.

---

## Paste this

```
Walk one batch through the legacy system end to end, live. Use Type 01,
scenario valid-minimal.

Before you run it, tell me in one line what each component does and which SFTP
role it authenticates as. Then run it. Then show me exactly what it left behind
and explain why those are artifacts rather than logs.
```

---

## What it does

Runs `make run TYPE=01 SCENARIO=valid-minimal`, then opens the evidence packet in
`evidence/B202607230000001/` — thirteen artifacts.

## The journey to narrate while it runs

```
gen/output/          DataGen writes an immutable bundle
   ↓ publisher       authenticates as raw-publisher — can write ONE zone
raw/incoming/        manifest written LAST — the readiness signal
   ↓ intake          claims by rename: posix_rename, atomic
raw/processing/
   ↓ processor       Java 21, in a container
csv/outgoing/        sanitized — no PAN, no clear CPF
   ↓ loader          never sees raw/ at all
staging → legacy → reporting
   ↓ operator        the only role that may archive
raw/archive/
```

## Three lines worth saying

> "Manifest-last is the synchronisation primitive. There is no lock and none is
> needed — a consumer treats the manifest's presence as *this batch is complete*."

> "The loader **cannot see the raw files at all.** Not by policy — by `chown`.
> When someone asks how you know the loader cannot leak a card number, the answer
> is not a code review. It is the filesystem."

> "Every batch leaves an evidence packet. Not logs — **artifacts.** This is what
> makes an autonomous run reviewable the next morning."

## The optional beat, if you have the time

```
cut -d, -f1,6,7,8,10 \
  contracts/types/01-card-settlement/main/expected-sanitized.csv | column -t -s,
```

```
batch_id          card_token                    card_last4  cpf_masked   amount_brl
B202607230000001  tok_0c5ac34fdde4aa92c6115f09  1111        *******8909  123.45
```

> "`tok_0c5ac34f…` and `*******8909`. The card number and the document never got
> past Java. And that boundary is checked byte-for-byte against a human-approved
> file — not with a regex that says *looks tokenised*."
