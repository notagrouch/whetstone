# Humanizer banned-tokens grep

The AI-tell vocabulary list. Run this grep on narration drafts before declaring them done. Empty result is necessary, NOT sufficient — the patterns NOT in the grep (em-dashes, rule-of-three, status-flattery) need a separate human pass.

## The grep

```bash
grep -iE "delve|leverage|robust|vibrant|tapestry|comprehensive|seamless|in the realm of|landscape|when it comes to|it's important to note|i hope this helps|ultimately,|in conclusion|moreover,|furthermore,|additionally," <draft-file>
```

## Why each token is on the list

| Token | Why it's AI-slop |
|---|---|
| `delve` | Disproportionately frequent in LLM output; almost no native speaker says "delve into" outside academic writing |
| `leverage` | Corporate-flavored verb that LLMs over-prefer for plain "use" |
| `robust` | Empty intensifier that LLMs reach for instead of describing what's actually strong |
| `vibrant` | LLM travel-blog vocabulary; rarely earned |
| `tapestry` | Metaphor LLMs over-use ("rich tapestry of...") |
| `comprehensive` | LLMs use this to claim breadth they didn't actually demonstrate |
| `seamless` | Marketing word; almost never accurate |
| `in the realm of` | LLM transitional cliche |
| `landscape` | Strategy-deck word LLMs over-reach for |
| `when it comes to` | LLM hedge phrase; usually deletable |
| `it's important to note` | LLM meta-commentary; readers don't need to be told what's important |
| `i hope this helps` | LLM closing flourish; tells you nothing |
| `ultimately,` | LLM connective tissue; rarely earns the weight |
| `in conclusion` | LLM essay-structure tell |
| `moreover,` | LLM connective; native speakers say "also" or just start the next sentence |
| `furthermore,` | Same as moreover |
| `additionally,` | Same |

## What this grep does NOT catch

These need a separate human read pass:

- **Em-dash overuse.** Em-dashes are the single most reliable AI-slop tell. Replace with periods, commas, or rephrase.
- **Rule-of-three padding.** "Same trick. Same mechanism. Same answer." Cut to one. Or two. Three is the LLM tic.
- **"It's not just X — it's Y."** Construction tic. Rewrite into a direct statement.
- **Status-flattery closes.** "which already puts you ahead of most people using them." Cut. The reader doesn't need to be flattered.
- **Writerly preamble taglines.** "Three things you actually need to know about AI. The kind that hold up after the demo wears off." Get to the first thing. The tagline is throat-clearing.
- **Em-dash mid-sentence rhetorical pauses.** "That single shift — oracle to assistant — is the whole game." Rewrite as two sentences or use commas.

## How to use this in a TTS narration pipeline

1. Write the draft narration.
2. Run the grep. Fix any hits.
3. Read it aloud, listening specifically for em-dashes (they pause longer than commas in TTS and sound stagey).
4. Look for rule-of-three pile-ups visually. Cut.
5. Look for status-flattery in the closing 2 sentences. Cut.
6. Then run TTS.

If you skip steps 3-5 and just run the grep, your narration will pass the grep AND still sound like AI.

## Captured failure mode

In the source series production, the foundational chapter went through 4 narration revisions to remove em-dashes, rule-of-three pileups, AI-vocab, and a status-flattery closer. Every later chapter shipped through the same humanizer pass and the dead vocabulary stopped appearing in early drafts within 3 chapters — proof that the rules become habitual once the author has internalized them.
