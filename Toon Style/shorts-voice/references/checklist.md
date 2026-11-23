# Pre-Delivery Checklist

Run every item. Fix any failure before outputting. Do not print this checklist to the user.

## Facts (hard gate: any failure blocks delivery)
- [ ] Every name, date, number, place and quote in the script appears in the user's input.
- [ ] No joke, analogy or jab asserts a new factual claim. Comparisons to universally known things are fine.
- [ ] Arithmetic you added (per-day rates, ratios) is correct and uses only the user's numbers.
- [ ] Paraphrased dialogue is framed as paraphrase ("was like", "basically says") unless the user gave a real quote.
- [ ] The user's core point/intent survives. If they argued X, the script still argues X.
- [ ] Uncertain claims in the input keep their hedge ("historians estimate", "reportedly").

## Hook
- [ ] First sentence < 20 words.
- [ ] Curiosity trigger lands within the first 8 words; no setup clause first.
- [ ] Hook chosen by tournament: 5 drafts of different types, Truth = 5 for all finalists.
- [ ] Hook question is identified; core answer at ≥ 50% and final twist at ≥ 60%; the sting calls back to it.
- [ ] Premise (the weird/dark/surprising fact) stated within the first 30 words.
- [ ] No greeting, channel name, "in this video", "today we…", "have you ever wondered".
- [ ] A validation beat follows (or a deliberate reason to skip it, e.g. cold-open countdown).
- [ ] A concrete anchor (date, place, number, name, product, specific situation) appears within the first 4 sentences, taken from the input only (skip if the input has none).

## Structure
- [ ] One storyline only.
- [ ] Beats escalate: each is worse, weirder or bigger than the last.
- [ ] Open loop planted in the first 20% and paid off after the main re-hook.
- [ ] A micro-hook roughly every 60–80 words.
- [ ] One main re-hook between 55% and 75% of the script; two if over 300 words.
- [ ] No beat runs longer than 4 sentences.
- [ ] Transitions are 1–3 word pivots ("But," "So," "Thing is,"), not bridge sentences.
- [ ] Any planted detail ("remember them") is paid off.

## Pacing
- [ ] Median sentence 10–15 words.
- [ ] 12–30% of sentences are ≤ 6 words (not more: over-fragmenting breaks the voice).
- [ ] Never more than 2 fragments in a row.
- [ ] No sentence > 35 words.
- [ ] If available, run `python -I scripts/check_script.py <script.txt> <input.txt>` (narration only) and fix every FAIL.
- [ ] At least one rhetorical question answered immediately ("Why? Well, …").
- [ ] Length = input word count ±10%.

## Voice
- [ ] "You" appears in the first 4 sentences or the viewer is otherwise placed in the story.
- [ ] 1–3 slang/internet terms, natural not forced.
- [ ] Uses "basically/literally/actually" at most once each per ~80 words (no tic overload).
- [ ] Zero banned words: delve, tapestry, testament, intricate, pivotal, multifaceted, realm, embark, unravel, furthermore, moreover, notably, additionally, in conclusion, it is worth noting, a stark reminder.
- [ ] No encyclopedic phrasing ("marked by inner struggles", "showcased his brilliance", "a relentless cycle of…").

## Humor
- [ ] One joke beat every 3–5 sentences (half for serious topics).
- [ ] Every joke ≤ 12 words and sits right after the fact it reacts to.
- [ ] At least 3 different joke types used (understatement, anachronism, verdict, literal idiom, pun, list deflation, jab, mock dialogue, aside).
- [ ] No joke punches down at victims, the audience or vulnerable groups.
- [ ] Punch-up pass done: the 2 weakest jokes were rewritten 3 ways, or cut.
- [ ] One debatable first-person take is present (if the input supports a judgment), and it's an opinion, not a fact.
- [ ] No creator sentence copied verbatim beyond 4 words (stock phrases excepted).
- [ ] No signature phrase used more than once; no joke type twice in a row.
- [ ] Hook type, re-hook phrase and sting differ from the previous script in this session.
- [ ] Promo/health/finance/legal scripts: no claim inflated beyond the input's wording, and every caveat/disclaimer kept.

## Ending
- [ ] Last content line is a sting ≤ 15 words (irony, verdict, jab, or gut-punch).
- [ ] No recap, no moral, no "thanks for watching", no question to the viewer.
- [ ] Final line is the CTA alone, matched to platform (YouTube `Subscribe.`, TikTok/Reels `Follow for more.`, or the user's own CTA compressed). A "Next video…" tease only if supported by the input.

## Output format
- [ ] Sections in order: `## Diagnosis` (3–7 bullets) → `## Script` → `## Changelog` (4–8 bullets + length line) → `## Alternate hooks` (2, each with its type).
- [ ] Script is pure narration: no brackets, stage directions, visual cues, hashtags, emojis, bold, headings or notes.
- [ ] No deictic visual references ("this map", "these guys") unless the input mentions the visual.
- [ ] Questions to the user asked only if topic/goal was genuinely unclear.
