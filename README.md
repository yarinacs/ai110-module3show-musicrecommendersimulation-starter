# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This recommender loads a catalog of 18 songs from `data/songs.csv`, scores each one against a user's taste profile using a weighted point system, and returns the top 3 matches. Scoring rewards exact categorical matches (genre, mood) with fixed bonus points and uses continuous similarity math for numeric features (energy, valence, danceability) so that near-misses are still rewarded proportionally.

---

## How The System Works

### Features of Each `Song`
Each song in the system is described by the following features:
- **Genre**: The type of music (e.g., pop, rock, lofi).
- **Mood**: The emotional tone of the song (e.g., happy, chill, intense).
- **Energy**: A numerical value (0 to 1) representing how lively or calm the song feels.
- **Tempo**: The speed of the song in beats per minute (BPM).
- **Valence**: A numerical value (0 to 1) indicating how positive or happy the song feels.
- **Danceability**: A measure of how suitable the song is for dancing.
- **Acousticness**: A measure of how acoustic or natural the song sounds.

### Information in the `UserProfile`
The `UserProfile` stores the user's preferences, including:
- **Favorite Genre**: The type of music the user enjoys most.
- **Preferred Mood**: The emotional tone the user prefers in songs.
- **Desired Energy Level**: A target energy value (e.g., 0.8 for high energy).
- **Ideal Tempo Range**: The range of BPM the user prefers (e.g., 100–130 BPM).

### Algorithm Recipe — Finalized Scoring Rules

Each song is evaluated against the user's profile and earns points as follows:

| Rule | Points | Formula |
|------|--------|---------|
| Genre exact match | **+2.0** | `+2.0 if song.genre == user.genre` |
| Mood exact match | **+1.5** | `+1.5 if song.mood == user.mood` |
| Energy similarity | **+0.0 – 1.0** | `1.0 - abs(song.energy - user.target_energy)` |
| Valence similarity | **+0.0 – 0.75** | `0.75 * (1.0 - abs(song.valence - user.target_valence))` |
| Danceability similarity | **+0.0 – 0.50** | `0.50 * (1.0 - abs(song.danceability - user.target_danceability))` |

**Maximum possible score: 5.75**

**Why these weights?**
- Genre outweighs mood (2.0 vs 1.5) because genre is a hard structural category — a rock fan handed a pop song is more jarred than someone who wanted "happy" and got "relaxed."
- Continuous similarity formulas (`1 - abs(...)`) avoid cliff effects: a song with `energy = 0.80` when the target is `0.81` still scores near-perfect rather than zero.
- Valence reinforces the mood signal numerically; danceability acts as a fine-grained tiebreaker.
- `tempo_bpm` and `acousticness` are not scored yet because the user profile has no direct inputs for them.

### How Songs Are Recommended
1. The system calculates a score for **every** song in the catalog using the rules above.
2. All scored songs are sorted in descending order.
3. The **top 3** songs are returned as recommendations.

### Known Biases and Limitations

- **Genre dominance:** At +2.0 points, a genre match alone can outrank songs that are a perfect mood, energy, and valence fit but in a different genre. A great lo-fi track may never surface for a user who says "pop," even if it matches everything else. Consider lowering genre weight if cross-genre discovery is a goal.
- **Mood vocabulary mismatch:** Mood is matched as an exact string (`"chill"` ≠ `"relaxed"`). Closely related moods score zero for the mood rule, creating an artificial gap between songs that feel emotionally similar.
- **Catalog skew:** The 18-song catalog over-represents certain genres (lofi, pop) and moods. Users with preferences for underrepresented genres (e.g., classical, metal) will almost always receive lower-scoring recommendations, not because the algorithm is wrong, but because the data is sparse.
- **No diversity enforcement:** The system always picks the *closest* matches. A user could receive three nearly identical songs instead of a varied set, reducing the value of the recommendations.

### Example
#### User Preferences:
- Genre: Pop
- Mood: Happy
- Energy: 0.8
- Tempo: 120 BPM

#### Songs in the Catalog:
| Title               | Genre | Mood   | Energy | Tempo | Score |
|---------------------|-------|--------|--------|-------|-------|
| Sunrise City        | Pop   | Happy  | 0.82   | 118   | 4.75  |
| Midnight Coding     | Lofi  | Chill  | 0.42   | 78    | 2.10  |
| Gym Hero            | Pop   | Intense| 0.93   | 132   | 3.90  |

#### Recommendations:
1. **Sunrise City** (Score: 4.75)
2. **Gym Hero** (Score: 3.90)
3. **Midnight Coding** (Score: 2.10)

This process ensures that the user receives personalized recommendations based on their preferences.

---

## User Profiles

Six profiles were run to evaluate the recommender — three standard taste profiles and three adversarial edge cases designed to expose weaknesses in the scoring logic.

### Standard Profiles

| Profile | Genre | Mood | Energy | Notes |
|---------|-------|------|--------|-------|
| Deep Focus | lofi | focused | 0.42 | Low-energy, acoustic, work/study listener |
| High-Energy Pop | pop | happy | 0.85 | Upbeat, danceable, festival listener |
| Deep Intense Rock | rock | intense | 0.90 | Heavy, fast, guitar-driven listener |

### Adversarial / Edge-Case Profiles

| Profile | Genre | Mood | Energy | Why adversarial |
|---------|-------|------|--------|----------------|
| Conflicted Listener | metal | sad | 0.90 | High energy + sad mood are in direct tension |
| Genre Desert | country | nostalgic | 0.35 | "country" does not exist in the catalog — genre bonus can never fire |
| All-Zeros Extremist | classical | melancholic | 0.0 | Every numeric target is 0.0 — an unreachable extreme |

---

## Sample Output

Running `PYTHONPATH=src python src/main.py` produces the following terminal output:

### Profile 1 — Deep Focus (lofi / focused)

> **Screenshot:** *(replace with your terminal screenshot)*

```
============================================================
  Profile : Deep Focus (lofi / focused)
  Genre   : lofi  |  Mood: focused
============================================================
  #1  Focus Flow — LoRoom
      Score : 5.71 / 5.75
        • genre match (+2.0)
        • mood match (+1.5)
        • energy similarity (+0.98)
        • valence similarity (+0.74)
        • danceability similarity (+0.49)

  #2  Midnight Coding — LoRoom
      Score : 4.22 / 5.75
        • genre match (+2.0)
        • energy similarity (+1.00)
        • valence similarity (+0.72)
        • danceability similarity (+0.50)

  #3  Library Rain — Paper Lanterns
      Score : 4.16 / 5.75
        • genre match (+2.0)
        • energy similarity (+0.93)
        • valence similarity (+0.75)
        • danceability similarity (+0.48)

  #4  Coffee Shop Stories — Slow Stereo
      Score : 2.08 / 5.75
        • energy similarity (+0.95)
        • valence similarity (+0.67)
        • danceability similarity (+0.46)

  #5  Old Porch Hymn — River Dust
      Score : 2.06 / 5.75
        • energy similarity (+0.89)
        • valence similarity (+0.74)
        • danceability similarity (+0.43)

------------------------------------------------------------
```

**Observation:** Focus Flow is a near-perfect match (5.71/5.75) — the only song with both genre *and* mood alignment. Scores drop sharply to ~4.2 once mood match disappears, showing the +1.5 bonus has real ranking power.

---

### Profile 2 — High-Energy Pop (pop / happy)

> **Screenshot:** *(replace with your terminal screenshot)*

```
============================================================
  Profile : High-Energy Pop (pop / happy)
  Genre   : pop  |  Mood: happy
============================================================
  #1  Sunrise City — Neon Echo
      Score : 5.70 / 5.75
        • genre match (+2.0)
        • mood match (+1.5)
        • energy similarity (+0.97)
        • valence similarity (+0.73)
        • danceability similarity (+0.49)

  #2  Gym Hero — Max Pulse
      Score : 4.09 / 5.75
        • genre match (+2.0)
        • energy similarity (+0.92)
        • valence similarity (+0.71)
        • danceability similarity (+0.46)

  #3  Rooftop Lights — Indigo Parade
      Score : 3.64 / 5.75
        • mood match (+1.5)
        • energy similarity (+0.91)
        • valence similarity (+0.74)
        • danceability similarity (+0.49)

  #4  Crown the Block — MC Velvet
      Score : 2.08 / 5.75
        • energy similarity (+0.93)
        • valence similarity (+0.68)
        • danceability similarity (+0.48)

  #5  Pulse Horizon — Wavecraft
      Score : 2.04 / 5.75
        • energy similarity (+0.90)
        • valence similarity (+0.70)
        • danceability similarity (+0.44)

------------------------------------------------------------
```

**Observation:** Rooftop Lights (#3) earns the mood bonus (+1.5) but *not* the genre bonus because its genre is `indie pop`, not `pop` — a visible effect of exact-string matching. It still ranks above Crown the Block which has neither categorical match.

---

### Profile 3 — Deep Intense Rock (rock / intense)

> **Screenshot:** *(replace with your terminal screenshot)*

```
============================================================
  Profile : Deep Intense Rock (rock / intense)
  Genre   : rock  |  Mood: intense
============================================================
  #1  Storm Runner — Voltline
      Score : 5.74 / 5.75
        • genre match (+2.0)
        • mood match (+1.5)
        • energy similarity (+0.99)
        • valence similarity (+0.75)
        • danceability similarity (+0.49)

  #2  Gym Hero — Max Pulse
      Score : 3.39 / 5.75
        • mood match (+1.5)
        • energy similarity (+0.97)
        • valence similarity (+0.53)
        • danceability similarity (+0.39)

  #3  Night Drive Loop — Neon Echo
      Score : 2.05 / 5.75
        • energy similarity (+0.85)
        • valence similarity (+0.74)
        • danceability similarity (+0.46)

  #4  Iron Collapse — Shatterglass
      Score : 1.88 / 5.75
        • energy similarity (+0.93)
        • valence similarity (+0.55)
        • danceability similarity (+0.40)

  #5  Crown the Block — MC Velvet
      Score : 1.85 / 5.75
        • energy similarity (+0.88)
        • valence similarity (+0.57)
        • danceability similarity (+0.40)

------------------------------------------------------------
```

**Observation:** Storm Runner dominates at 5.74/5.75 — the highest score of all six profiles, because it perfectly aligns on both genre+mood (+3.5) and energy (0.91 vs target 0.90). There is only one rock song in the catalog, so positions #3–#5 all fall below 2.1, illustrating catalog skew.

---

### Adversarial Profile 1 — Conflicted Listener (metal / sad, energy=0.9)

> **Screenshot:** *(replace with your terminal screenshot)*

```
============================================================
  Profile : [ADVERSARIAL] Conflicted Listener (metal / sad, energy=0.9)
  Genre   : metal  |  Mood: sad
============================================================
  #1  Iron Collapse — Shatterglass
      Score : 4.17 / 5.75
        • genre match (+2.0)
        • energy similarity (+0.93)
        • valence similarity (+0.73)
        • danceability similarity (+0.50)

  #2  Empty Glass — Dara Bell
      Score : 3.21 / 5.75
        • mood match (+1.5)
        • energy similarity (+0.48)
        • valence similarity (+0.74)
        • danceability similarity (+0.49)

  #3  Storm Runner — Voltline
      Score : 1.93 / 5.75
        • energy similarity (+0.99)
        • valence similarity (+0.54)
        • danceability similarity (+0.40)

  #4  Night Drive Loop — Neon Echo
      Score : 1.74 / 5.75
        • energy similarity (+0.85)
        • valence similarity (+0.53)
        • danceability similarity (+0.36)

  #5  Gym Hero — Max Pulse
      Score : 1.58 / 5.75
        • energy similarity (+0.97)
        • valence similarity (+0.32)
        • danceability similarity (+0.29)

------------------------------------------------------------
```

**What this reveals:** The system can be "tricked" by conflicting signals. Iron Collapse wins on genre match alone (+2.0) despite having *angry* mood, not *sad*. Empty Glass is the only sad song in the catalog, but its low energy (0.38) clashes with the target of 0.9, costing it ~0.52 energy points. The mood bonus is not strong enough to overcome the energy mismatch — the conflicting user profile produces a winner that satisfies genre but not mood.

---

### Adversarial Profile 2 — Genre Desert (country / nostalgic)

> **Screenshot:** *(replace with your terminal screenshot)*

```
============================================================
  Profile : [ADVERSARIAL] Genre Desert (country / nostalgic)
  Genre   : country  |  Mood: nostalgic
============================================================
  #1  Old Porch Hymn — River Dust
      Score : 3.69 / 5.75
        • mood match (+1.5)
        • energy similarity (+0.96)
        • valence similarity (+0.74)
        • danceability similarity (+0.49)

  #2  Library Rain — Paper Lanterns
      Score : 2.19 / 5.75
        • energy similarity (+1.00)
        • valence similarity (+0.73)
        • danceability similarity (+0.46)

  #3  Coffee Shop Stories — Slow Stereo
      Score : 2.14 / 5.75
        • energy similarity (+0.98)
        • valence similarity (+0.68)
        • danceability similarity (+0.48)

  #4  Focus Flow — LoRoom
      Score : 2.13 / 5.75
        • energy similarity (+0.95)
        • valence similarity (+0.73)
        • danceability similarity (+0.45)

  #5  Spacewalk Thoughts — Orbit Bloom
      Score : 2.11 / 5.75
        • energy similarity (+0.93)
        • valence similarity (+0.73)
        • danceability similarity (+0.45)

------------------------------------------------------------
```

**What this reveals:** No song ever receives the +2.0 genre bonus — the maximum achievable score drops to 3.75. Old Porch Hymn wins on mood alone (+1.5), but positions #2–#5 are separated by tiny margins (2.19 vs 2.11), making the ranking essentially arbitrary. A missing genre means the system is navigating blind, surfacing acoustically-similar songs regardless of actual style fit.

---

### Adversarial Profile 3 — All-Zeros Extremist (classical / melancholic)

> **Screenshot:** *(replace with your terminal screenshot)*

```
============================================================
  Profile : [ADVERSARIAL] All-Zeros Extremist (classical / melancholic)
  Genre   : classical  |  Mood: melancholic
============================================================
  #1  Autumn Sonata No. 3 — Clara Voss
      Score : 5.20 / 5.75
        • genre match (+2.0)
        • mood match (+1.5)
        • energy similarity (+0.78)
        • valence similarity (+0.54)
        • danceability similarity (+0.38)

  #2  Empty Glass — Dara Bell
      Score : 1.50 / 5.75
        • energy similarity (+0.62)
        • valence similarity (+0.59)
        • danceability similarity (+0.29)

  #3  Spacewalk Thoughts — Orbit Bloom
      Score : 1.28 / 5.75
        • energy similarity (+0.72)
        • valence similarity (+0.26)
        • danceability similarity (+0.30)

  #4  Old Porch Hymn — River Dust
      Score : 1.24 / 5.75
        • energy similarity (+0.69)
        • valence similarity (+0.29)
        • danceability similarity (+0.26)

  #5  Library Rain — Paper Lanterns
      Score : 1.16 / 5.75
        • energy similarity (+0.65)
        • valence similarity (+0.30)
        • danceability similarity (+0.21)

------------------------------------------------------------
```

**What this reveals:** The system handles zeros without crashing or going negative (the `1.0 - abs(...)` formula always stays in [0, 1]). However, the winner (Autumn Sonata) scores 5.20 purely from its genre+mood categorical matches — the numeric targets are so extreme (0.0) that *every* song loses energy/valence/danceability points and the ranking collapses into "whoever has categorical matches wins." The all-zeros profile does not meaningfully test numeric fit.

---

**Summary of what the adversarial runs revealed:**
- **Conflicted Listener:** Categorical genre bonus (2.0) can override a mood mismatch. High-energy + sad mood produces a winner that matches neither signal perfectly.
- **Genre Desert:** Without a genre match, max achievable score is only 3.75 and the top-4 recommendations are nearly tied — the ranking is fragile.
- **All-Zeros Extremist:** Extreme numeric targets don't break the math (no negatives) but they make numeric similarity meaningless, leaving categorical matches as the only real discriminator.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

The most important thing I learned is that a recommender system is really a set of opinions encoded as numbers. When I doubled the energy weight from 1.0 to 2.0, "Gym Hero" — a loud workout track — started showing up for users who said they wanted happy pop music. That result came from one changed number, not a bug. It showed that weight choices quietly decide whose preferences the system takes seriously.

I also learned that bias does not always look like an error. The Genre Desert profile (a country fan getting folk and lofi suggestions instead) produced plausible-sounding results — songs that are acoustically similar — while completely ignoring what the user actually asked for. The system had no way to say "I don't have what you want." It just filled the gap silently. That is how real recommender systems behave too, and it is easy to miss unless you deliberately test edge cases.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

