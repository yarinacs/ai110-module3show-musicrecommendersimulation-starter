# Reflection: Profile Pair Comparisons

Each section below compares two user profiles side by side — what they asked for, what the system gave them, and whether that makes sense.

---

## Pair 1: Deep Focus (lofi/focused) vs. High-Energy Pop (pop/happy)

These two profiles are opposites. The lofi listener wants calm, quiet, low-energy music to study to — think rain sounds and soft piano. The pop listener wants loud, upbeat, danceable songs.

The lofi profile correctly surfaces the three lofi songs (Focus Flow, Midnight Coding, Library Rain) near the top, because they match both genre and energy level. That feels right.

The pop profile, however, also surfaces "Gym Hero" — a pop song explicitly tagged as *intense*, not *happy*. Why? Because the scoring system only checks whether the genre tag says "pop" and whether the energy level is close to the target. "Gym Hero" has energy 0.93, which is very close to the pop profile's target of 0.85, so it earns a big score boost from that alone. The system doesn't understand that a gym bro track and a cheerful pop song feel completely different to a human listener — they both say "pop" and both have high energy, so the system treats them as nearly identical.

The key difference between these profiles: **lofi listeners get well-matched results because there are three lofi songs in the catalog; pop listeners get slightly mismatched results because the two pop songs span very different moods (happy vs. intense), and the energy scoring can't tell those apart.**

---

## Pair 2: High-Energy Pop (pop/happy) vs. Deep Intense Rock (rock/intense)

Both profiles want high-energy music (targets: 0.85 and 0.90 respectively), but they have very different genre and mood expectations.

The pop profile gets "Sunrise City" (pop/happy) as its top result — a genuine match on all three of genre, mood, and energy. That is exactly correct.

The rock profile gets "Storm Runner" (rock/intense) at #1 — also a genuine match. But the next four recommendations diverge interestingly: the system fills slots 2–5 with whatever song has energy closest to 0.90, regardless of genre. "Gym Hero" (pop/intense) ranks #2 for the rock profile because its energy (0.93) is nearly identical to the rock target and it shares the "intense" mood bonus. A real rock fan would find a pop gym track at #2 baffling.

The comparison illustrates that **high energy is high energy to this system**. Both pop and rock fans end up with very similar songs in positions 2–5 because energy is the heaviest scoring term. The genre label only separates the top position; everything after that is a shared high-energy pool.

---

## Pair 3: Deep Intense Rock (rock/intense) vs. Conflicted Listener (metal/sad, energy=0.9)

Both profiles want aggressive, high-energy sound, but the Conflicted Listener adds a contradiction: they list "sad" as their mood and "metal" as their genre.

The rock profile gets sensible results — Storm Runner at #1, then high-energy songs filling out the rest.

The Conflicted Listener profile reveals a real tension in the scoring. "Sad" mood only matches one song in the entire catalog: "Empty Glass" (soul/sad, energy 0.38). But Empty Glass has energy 0.38, far from the target of 0.90 — so the mood bonus (+1.5) is partially cancelled out by a big energy penalty. Meanwhile, "Iron Collapse" (metal/angry, energy 0.97) matches the genre tag and is very close in energy, so it likely floats to the top despite having the wrong mood. The system essentially ignores the stated mood preference in favor of energy proximity.

This comparison shows that **when a user's mood and energy preferences contradict each other, energy wins**. A person who says they want "sad metal" would probably expect dark, heavy songs — but the system may serve them euphoric EDM if the energy number happens to be closer.

---

## Pair 4: Genre Desert (country/nostalgic) vs. All-Zeros Extremist (classical/melancholic)

Both profiles expose catalog weaknesses rather than scoring logic flaws.

The Genre Desert profile requests "country" — a genre that doesn't exist in the 18-song dataset. This means the genre bonus (worth +1.0 points) fires for zero songs across the entire catalog. The profile falls back entirely on mood matching (nostalgic) and numeric similarity. "Old Porch Hymn" (folk/nostalgic) likely ranks highest because it matches mood and has low energy and high acousticness, even though folk and country are distinct genres that a real listener would not treat as interchangeable.

The All-Zeros profile sets every numeric target to 0.0 — an extreme that no real song reaches. The scoring formula rewards whichever songs have the lowest energy, valence, and danceability, so very quiet songs like Autumn Sonata (classical/melancholic, energy 0.22) and Spacewalk Thoughts (ambient/chill, energy 0.28) float to the top. Autumn Sonata also earns the genre and mood bonus (+2.5 combined), making it the clear winner.

The comparison shows **two very different failure modes**: the country profile fails because the catalog is missing its genre entirely, while the all-zeros profile actually works reasonably well because "lowest energy" maps naturally to a small subset of calm songs. A country fan gets zero relevant recommendations; the extreme-minimalist listener accidentally gets decent ones.

---

## Summary

Across all four comparisons, the most consistent theme is that **energy is the dominant force in the scoring system**. It earns up to 2.0 points — more than any other single term — which means two very different songs (like a sad soul track and an angry metal track) can end up with identical scores if they happen to share a similar energy value. Genre and mood bonuses matter most when a song is an exact match, but once you move past the top result, energy proximity takes over and creates a kind of high-energy or low-energy "bucket" that overrides musical style.
