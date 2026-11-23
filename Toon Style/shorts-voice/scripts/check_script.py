"""Measure a rewritten script against the shorts-voice numeric rules.

Usage: python -I check_script.py <script.txt> [input.txt]
The script file must contain narration only (no Diagnosis/Changelog).
Thresholds are calibrated on the creator's 40 Group A scripts (middle-50% range).
FAIL = must fix. WARN = allowed, but mention why in the changelog.
"""
import re
import sys

BANNED = ["delve", "tapestry", "testament", "intricate", "pivotal", "multifaceted",
          "realm", "embark", "unravel", "furthermore", "moreover", "notably",
          "additionally", "in conclusion", "it is worth noting", "a stark reminder",
          "in this video", "today we", "have you ever wondered", "let's dive",
          "hey guys", "welcome back", "without further ado", "stay tuned",
          "let me know in the comments", "game-changer", "you won't believe"]
REHOOKS = ["part nobody", "gets expensive", "part that actually", "here's the", "even weirder", "the worst part", "craziest part", "juicy part",
           "terrifying part", "darkest part", "this is really funny", "but here's",
           "things got", "turns out", "and i kid you not"]
WPS = 3.1


def sentences(text):
    return [s for s in re.split(r"(?<=[.?!])\s+", text.strip()) if s.strip()]


def words(text):
    return re.findall(r"[A-Za-z0-9'’,.%-]+", text)


def main():
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"\[(music|clears throat)\]|>>", "", raw)  # transcript noise
    body = re.sub(r"\s*(Subscribe|Follow)[^.]*\.\s*$", "", text.strip())
    sents = sentences(body)
    lens = [len(words(s)) for s in sents]
    srt = sorted(lens)
    median = srt[len(srt) // 2]
    total = len(words(text))
    low = text.lower()
    fails, warns = [], []

    short = sum(1 for n in lens if n <= 6) / len(lens)
    run = best = 0
    for n in lens:
        run = run + 1 if n <= 6 else 0
        best = max(best, run)

    print(f"words: {total}  (~{total / WPS:.0f}s at {WPS} wps)")
    print(f"sentences: {len(sents)}  median: {median}  avg: {sum(lens) / len(lens):.1f}  max: {srt[-1]}")
    print(f"<=6-word sentences: {short:.0%}  longest fragment run: {best}")
    print(f"first sentence: {lens[0]} words  |  sting (last content sentence): {lens[-1]} words")

    if lens[0] >= 20: fails.append("first sentence >= 20 words")
    if not 10 <= median <= 15: fails.append("median sentence outside 10-15 words")
    if short < 0.12: fails.append("under 12% of sentences are <= 6 words (too flat)")
    if short > 0.30: fails.append("over 30% of sentences are <= 6 words (too choppy)")
    if best > 2: fails.append(f"{best} fragments in a row (max 2)")
    if srt[-1] > 35: fails.append("a sentence is longer than 35 words")
    if lens[-1] > 15: fails.append("sting (last content sentence) > 15 words")
    for b in BANNED:
        if b in low: fails.append(f"banned phrase: {b}")
    if re.search(r"[\[\]]|\*\*|^#", raw, re.M): fails.append("contains brackets/markup")

    hits = sorted((m.start() / len(low), r) for r in REHOOKS for m in re.finditer(re.escape(r), low))
    if hits:
        print("hook/re-hook phrases at: " + ", ".join(f"'{r}' {p:.0%}" for p, r in hits))
    main = [h for h in hits if 0.5 <= h[0] <= 0.8]
    if total > 150 and not main:
        warns.append("no main re-hook phrase between 50% and 80%")
    if "?" not in body: warns.append("no rhetorical question")
    if " you" not in " " + " ".join(sents[:4]).lower(): warns.append("no 'you' in first 4 sentences")
    if not re.search(r"(subscribe|follow)[^.]*\.\s*$", low.strip()): warns.append("does not end with Subscribe/Follow CTA (fine if user supplied their own CTA)")

    if len(sys.argv) > 2:
        src = len(words(open(sys.argv[2], encoding="utf-8").read()))
        ratio = total / src
        print(f"length vs input: {src} -> {total} ({ratio:.0%})")
        if not 0.9 <= ratio <= 1.1: fails.append("length outside input +/-10%")

    if warns: print("\nWARN:\n- " + "\n- ".join(warns))
    print("\nPASS" if not fails else "\nFAIL:\n- " + "\n- ".join(fails))


if __name__ == "__main__":
    main()
