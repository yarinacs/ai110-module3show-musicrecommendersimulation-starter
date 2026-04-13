# Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeMatch 1.0**

A rule-based music recommender that matches songs to a listener based on their taste profile.

---

## 2. Intended Use

VibeMatch is designed for classroom exploration of how recommender systems work. It takes a user's music preferences — genre, mood, energy level, and a few other traits — and returns the five best-matching songs from a small catalog.

It assumes the user can describe their taste with exact labels (like "lofi" or "chill") and numeric targets (like an energy level between 0 and 1). It is not designed for real users on a real platform. It is a learning tool, not a product.

**Not intended for:** commercial music apps, large catalogs, real user data, or any situation where fairness to all listeners actually matters.

---

## 3. How the Model Works

Every song in the catalog gets a score based on how well it matches the user's preferences. The score has five parts:

1. **Genre match** — if the song's genre matches what the user likes, it gets +1.0 point.
2. **Mood match** — if the song's mood matches (e.g., "chill," "happy," "intense"), it gets +1.5 points.
3. **Energy similarity** — the closer the song's energy level is to the user's target, the more points it earns (up to +2.0).
4. **Valence similarity** — valence measures how positive or upbeat a song feels. Closer to target = more points (up to +0.75).
5. **Danceability similarity** — how rhythmically easy the song is to move to. Closer to target = more points (up to +0.50).

The maximum possible score is 5.75. The five highest-scoring songs are returned as recommendations.

One change from the original starter code: the energy weight was doubled from 1.0 to 2.0 to make it the strongest signal. Genre was also reduced from 2.0 to 1.0 to prevent exact genre matches from always dominating.

---

## 4. Data

The catalog has **18 songs**. Each song has these features: title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness.

**Genres included:** lofi, pop, rock, ambient, jazz, synthwave, hip-hop, indie pop, classical, r&b, metal, folk, reggae, edm, soul

**Moods included:** happy, chill, intense, relaxed, focused, moody, confident, melancholic, romantic, angry, nostalgic, peaceful, euphoric, sad

**Limits of the dataset:**
- Lofi has 3 songs; pop has 2. Every other genre has exactly 1.
- There is no country, blues, Latin, or K-pop.
- The catalog is too small to give meaningful variety to users with niche tastes.
- No data was added or removed from the original starter set.

---

## 5. Strengths

The system works best when the user's preferred genre is well-represented in the catalog. Lofi listeners consistently get reasonable top-5 results because there are three lofi songs to choose from, and the scoring logic correctly separates low-energy acoustic songs from high-energy electronic ones on the energy axis.

It also handles clear opposites well. A listener who wants very low energy (like 0.2) will never be recommended a high-energy metal track, because the energy penalty is steep enough to bury it. The intuition that "calm music goes to calm users" holds reliably.

When genre and mood both match — like the rock/intense profile getting Storm Runner at #1 — the top result almost always makes sense and aligns with what a human listener would expect.

---

## 6. Limitations and Bias

The scoring formula gives energy similarity a weight of 2.0 — twice the weight of genre (1.0) and greater than mood (1.5) — which causes the system to over-prioritize energy proximity over a user's stated genre preference. For users whose favorite genre is rare in the dataset (e.g., reggae, metal, and EDM each have only one song), the genre match bonus applies to just one candidate while the energy bonus applies to all eighteen songs; as a result, their top-5 results are dominated by energy-matched songs from unrelated genres rather than their actual preference. Additionally, the `acousticness` dimension is collected in the user profile but is completely excluded from the scoring function, meaning users who prefer acoustic-style music receive no differentiation between a high-acousticness folk track and a low-acousticness EDM track that happen to share similar energy and valence values. This creates a filter bubble for acoustic listeners: the system will systematically surface electronically produced songs over acoustic ones, even when the user has explicitly flagged an acoustic preference. Taken together, the energy-dominated scoring and missing acousticness term make the recommender most fair for users whose preferred genre is well-represented in the dataset (lofi, pop) and least fair for users with niche genre tastes or a strong preference for acoustic music.

---

## 7. Evaluation

Six user profiles were tested: a **Deep Focus lofi listener** (low energy, acoustic), a **High-Energy Pop listener** (upbeat, danceable), a **Deep Intense Rock listener** (aggressive, loud, fast), and three adversarial edge cases — a **Conflicted Listener** (high energy but sad mood), a **Genre Desert listener** (requests "country," which does not exist in the catalog), and an **All-Zeros Extremist** (every numeric target set to 0.0).

The most surprising result came from the High-Energy Pop profile: "Gym Hero" — a song explicitly tagged as *intense*, not *happy* — ranked second behind "Sunrise City." This happened because the energy scoring is weighted so heavily (2.0 points) that a song with nearly identical energy to the target gets a large score boost, even if its mood tag is completely wrong. To a regular listener, "Gym Hero" is a workout track, not a happy pop song — but the system only sees that the numbers are close and the genre label matches, so it confidently recommends it.

The Deep Intense Rock profile revealed a second surprise: "Iron Collapse" (a metal track) ranked *below* "Night Drive Loop" (synthwave) in positions 3 and 4. Intuitively, metal is far closer to rock than synthwave is — but the system has no concept of genre families. Once a song misses the genre bonus, it competes on valence and danceability alone, and Night Drive Loop happened to have a valence (0.49) nearly identical to the rock profile's target (0.48), while Iron Collapse's valence (0.22) was a poor match. The system doesn't know that metal and rock belong to the same musical family.

The Genre Desert profile (country/nostalgic) confirmed the catalog skew problem: with no country songs available, the profile received zero genre bonus points across all 18 songs. The top results were driven entirely by low energy and high acousticness proximity, landing on folk and lofi tracks that happen to feel similar but were never the user's stated preference. A country fan would be frustrated to receive zero country recommendations.

---

## 8. Ideas for Improvement

**1. Add acousticness to the score.**
The user profile already stores acousticness preference and a `likes_acoustic` flag — but neither is used in scoring. Adding an acousticness similarity term (similar to the energy term) would immediately improve results for folk, classical, and lofi listeners who prefer organic-sounding music over electronic production.

**2. Replace exact genre matching with genre families.**
Right now, "lofi" and "ambient" score the same as "lofi" and "metal" when the genre doesn't match — both get zero. Grouping related genres (e.g., lofi + ambient + jazz = "chill/acoustic family") and giving partial credit would make the system more forgiving and more useful for listeners whose taste crosses genre lines.

**3. Include tempo as a preference.**
Tempo (BPM) is in the dataset but completely ignored by the scoring function. A user who wants slow background music (60–80 BPM) and a user who wants fast dance music (140+ BPM) would currently receive nearly identical recommendations if their energy targets happen to match. Adding a tempo preference field and a small scoring term for tempo proximity would sharply improve recommendations at the extremes.

---

## 9. Personal Reflection

**Biggest learning moment**

The biggest surprise came from changing a single number. When the energy weight was doubled from 1.0 to 2.0, "Gym Hero" — a loud, intense workout track — started appearing in the top results for users who said they wanted happy pop music. Nothing else changed. No new code, no new data. Just one number. That moment made it obvious that weight choices are not neutral technical decisions. They are value judgments about what the system thinks matters most. A tiny tuning change quietly reshaped whose preferences got honored.

**How AI tools helped — and when to double-check**

AI tools were useful for spotting patterns I might have missed on my own. For example, pointing out that `acousticness` was stored in the user profile but never actually used in the scoring function was something that's easy to overlook when you're deep in the code. AI can scan across the whole codebase and flag that kind of inconsistency quickly.

That said, the explanations needed checking. When an AI described *why* Iron Collapse ranked below Night Drive Loop, the reasoning was correct — but only because I could verify it against the actual score math in `score_song`. If I had just trusted the explanation without reading the formula, I might have misunderstood what was actually happening. AI tools are good at summarizing; the engineering judgment still has to come from you.

**Why simple math can still feel like a recommendation**

The scoring formula is just addition and subtraction. There is no learning, no neural network, no "understanding" of music. Yet when Focus Flow scored 5.71 out of 5.75 for a lofi/focused listener, it felt completely right. A study-music fan would genuinely enjoy that song. The reason it works is that the features — energy, mood, genre — are already good proxies for what humans care about. The math is simple, but the features were chosen thoughtfully. That is the real work. A recommender is only as good as the signals you choose to measure, not how clever your formula is.

**What I would try next**

If I kept developing this, the first thing I would add is acousticness to the score. The data is already there — it just needs to be wired up. Second, I would test what happens when you show users their score breakdown and ask them to rate whether the recommendation felt right. That kind of feedback loop is how real systems learn over time. Finally, I would want to add a diversity rule so the top five results cannot all come from the same energy bucket — because right now a high-energy user could receive five nearly identical songs and call it a "recommendation."
