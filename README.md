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

## Sample Output

Running `PYTHONPATH=src python src/main.py` produces the following terminal output:

```
Loaded songs: 18

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

============================================================
  Profile : Upbeat Pop (pop / happy)
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

**What to notice:**
- **Focus Flow** scores 5.71/5.75 — the only song matching both genre *and* mood for the lofi profile, with near-perfect numerical alignment.
- **Rooftop Lights** (#3 pop/happy) earns the mood bonus (+1.5) but *not* the genre bonus because its genre is `indie pop`, not `pop` — a visible effect of exact-string matching.
- Scores drop sharply after #3 in both profiles, confirming the genre+mood bonuses dominate the ranking.

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

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


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

