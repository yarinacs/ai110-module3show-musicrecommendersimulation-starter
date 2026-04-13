from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py

    Numerical targets (energy, valence, danceability, acousticness) mirror the
    Song fields so a recommender can compute distance directly between the
    profile vector and each song vector.

    CRITIQUE NOTE — can this profile distinguish "intense rock" vs "chill lofi"?
    YES, but only because all four numerical fields are present together:
      - energy alone puts Storm Runner (0.91) far from Library Rain (0.35), so a
        low target_energy already separates them.
      - acousticness is the decisive second axis: rock sits near 0.10 while lofi
        sits near 0.71-0.86.  A profile that omits acousticness would mis-score
        any low-energy electronic track the same as a lofi track.
      - valence breaks ties between songs that happen to share similar energy
        (e.g. Night Drive Loop and Midnight Coding are both ~0.4-0.42 energy but
        differ in valence 0.49 vs 0.56).
    WHERE THE PROFILE IS STILL NARROW:
      - favorite_genre and favorite_mood are exact-match only.  A user who likes
        "lofi" gets zero partial credit for "ambient", even though both are chill
        low-energy styles.  Replacing these with weighted genre/mood families
        would improve coverage.
      - The profile has no tempo preference, so a 60-BPM ambient drone and a
        90-BPM jazz track could score identically.
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float
    target_acousticness: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int/float."""
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"],
                "mood":          row["mood"],
                "energy":        float(row["energy"]),
                "tempo_bpm":     float(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences (max 5.75) and return (score, reasons)."""
    score = 0.0
    reasons = []

    # --- Categorical matches (exact) ---
    if song["genre"].lower() == user_prefs["genre"].lower():
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    if song["mood"].lower() == user_prefs["mood"].lower():
        score += 1.5
        reasons.append(f"mood match (+1.5)")

    # --- Numerical similarity (continuous, range 0–1) ---
    energy_pts = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts:.2f})")

    valence_pts = 0.75 * (1.0 - abs(song["valence"] - user_prefs["target_valence"]))
    score += valence_pts
    reasons.append(f"valence similarity (+{valence_pts:.2f})")

    danceability_pts = 0.50 * (1.0 - abs(song["danceability"] - user_prefs["target_danceability"]))
    score += danceability_pts
    reasons.append(f"danceability similarity (+{danceability_pts:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest-first, and return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
