# Anchor flag schema

The reusable animation primitive vocabulary that emerged from production of the 8-chapter source series. Each anchor flag corresponds to a React component in the `ChapterReel` composition that takes the beat's content and renders an animated illustration.

## Schema

```typescript
type ChapterAnchor = {
  flag: AnchorFlag;       // which primitive renders this anchor
  body: string;            // the manuscript-derived teaching content
  carousel?: CarouselItem[]; // optional sub-primitive: list of example cards
  receipt?: string;        // optional citation / source / footnote
};

type AnchorFlag =
  | 'showPhoneAuto'            // chapter-specific (single-use)
  | 'showBellCurve'            // chapter-specific (single-use)
  | 'showOracleAssistant'      // chapter-specific (single-use)
  | 'showThreeChatbots'        // chapter-specific (single-use)
  | 'showTransformerTree'      // chapter-specific (single-use)
  | 'showWeekTimeline'         // chapter-specific (single-use)
  | 'showPromptComparison'     // REUSABLE — comparison cards (vague vs specific)
  | 'showNumberedChecklist'    // REUSABLE — numbered step list
  | 'showPushbackExamples'     // REUSABLE — quote-style examples
  | 'showContrastList'         // REUSABLE — A-vs-B list
  | 'exampleCarousel'          // SUB-PRIMITIVE — used inside any anchor for example rotation
  ;
```

## Reuse table

The reusable primitives drove iteration compression. Single-use primitives stayed in the chapter that defined them.

| Primitive | Chapters using | Reuse pattern |
|---|---|---|
| `exampleCarousel` | Ch2-8 (7 chapters) | Universal sub-primitive; appears inside almost every anchor |
| `showPushbackExamples` | Ch3, Ch4, Ch6, Ch7 (4 chapters) | Workhorse for objection / pitfall content |
| `showNumberedChecklist` | Ch3, Ch4, Ch7, Ch8 (4 chapters) | Workhorse for step lists / templates |
| `showContrastList` | Ch4, Ch5, Ch6 (3 chapters) | A-vs-B framing |
| `showPromptComparison` | Ch3, Ch5, Ch8 (3 chapters) | Two-column comparison |
| `showPhoneAuto` | Ch1 only | Single-use |
| `showBellCurve` | Ch1 only | Single-use |
| `showOracleAssistant` | Ch1 only | Single-use |
| `showThreeChatbots` | Ch2 only | Single-use |
| `showTransformerTree` | Ch2 only | Single-use |
| `showWeekTimeline` | Ch2 only | Single-use |

## When to build a new primitive vs. reuse

**Build new** when the teaching device is structurally unique to one chapter. A bell curve teaches distribution; a transformer tree teaches a hierarchical generation process. These don't reuse because no other chapter has that shape.

**Reuse** when the teaching shape is one of:
- Numbered steps → `showNumberedChecklist`
- Two-column comparison → `showPromptComparison` or `showContrastList`
- Quoted pushback / common objections → `showPushbackExamples`
- Carousel of varied examples illustrating one point → `exampleCarousel`

## Lesson from the inventory

Chapters 1-2 added 6 chapter-specific primitives that never reused. Chapters 3-4 added 4 primitives that became the workhorse vocabulary for the rest of the series. **After Chapter 4, no new primitives were added** — Chapters 5-8 were pure recombination.

The shape of "build new primitives early, reuse later" is what iteration compression looks like in code. If you're 5 chapters in and still adding new primitives, audit whether those primitives could be expressed in the existing reusable schema before committing them.

## Implementation note

In the source series, all primitive components live inline in one ~3200-line `ChapterReel.tsx` monolith, not as separate `.tsx` files. The monolith approach trades discoverability for fewer import chains and faster Remotion re-renders during dev. For a public skill, the recommendation is to split each primitive into its own file under `src/primitives/` once the inventory stabilizes — but DO NOT split prematurely; the monolith was the right call during primitive discovery.
