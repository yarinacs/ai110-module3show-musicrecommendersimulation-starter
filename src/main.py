"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # --- Taste Profile ---
    # This profile targets a "deep focus" listener: low-energy, acoustic-leaning,
    # positive but not euphoric.  All four numerical axes are included so the
    # recommender can compute a proper multi-dimensional distance rather than
    # relying on a single feature.
    #
    # Expected top matches in our dataset:
    #   Focus Flow (lofi/focused, energy 0.40)  ← genre + mood + all numerics align
    #   Midnight Coding (lofi/chill, energy 0.42)
    #   Library Rain (lofi/chill, energy 0.35, acousticness 0.86)
    #
    # Expected low matches:
    #   Iron Collapse (metal/angry, energy 0.97)  ← every axis is the opposite
    #   Storm Runner (rock/intense, energy 0.91, acousticness 0.10)
    #   Pulse Horizon (edm/euphoric, energy 0.95)
    #
    # "intense rock" vs "chill lofi" check:
    #   target_energy 0.42 pulls hard toward lofi and away from rock.
    #   target_acousticness 0.78 is the decisive second axis — rock scores ~0.10
    #   while lofi scores ~0.71-0.86.  Without acousticness in the profile, a low-
    #   energy electronic track would look identical to a lofi track.
    def print_recommendations(label: str, prefs: dict, k: int = 5) -> None:
        recommendations = recommend_songs(prefs, songs, k=k)
        width = 60
        print("\n" + "=" * width)
        print(f"  Profile : {label}")
        print(f"  Genre   : {prefs['genre']}  |  Mood: {prefs['mood']}")
        print("=" * width)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"  #{rank}  {song['title']} — {song['artist']}")
            print(f"      Score : {score:.2f} / 5.75")
            for reason in explanation.split(" | "):
                print(f"        • {reason}")
            print()
        print("-" * width)

    # --- Profile 1: Deep focus / lofi listener ---
    print_recommendations(
        label="Deep Focus (lofi / focused)",
        prefs={
            "genre": "lofi",
            "mood": "focused",
            "target_energy": 0.42,
            "target_valence": 0.60,
            "target_danceability": 0.62,
            "target_acousticness": 0.78,
            "likes_acoustic": True,
        },
    )

    # --- Profile 2: High-Energy Pop listener ---
    print_recommendations(
        label="High-Energy Pop (pop / happy)",
        prefs={
            "genre": "pop",
            "mood": "happy",
            "target_energy": 0.85,
            "target_valence": 0.82,
            "target_danceability": 0.80,
            "target_acousticness": 0.15,
            "likes_acoustic": False,
        },
    )

    # --- Profile 3: Deep Intense Rock ---
    # Targets heavy, high-energy guitar-driven tracks.
    # Expected top match: Storm Runner (rock/intense, energy 0.91, acousticness 0.10)
    # Low acousticness and high energy should clearly separate rock from lofi or ambient.
    #
    # WHY does Storm Runner rank #1? (Inline-chat style breakdown)
    # ─────────────────────────────────────────────────────────────
    # Storm Runner attributes (from songs.csv):
    #   genre="rock", mood="intense", energy=0.91, valence=0.48,
    #   danceability=0.66, acousticness=0.10
    #
    # score_song() math against this profile (target_energy=0.90, target_valence=0.48,
    #   target_danceability=0.65):
    #
    #   genre match ("rock" == "rock")           → +2.00   [60 % cap exhausted here]
    #   mood  match ("intense" == "intense")     → +1.50
    #   energy:  1.0 - |0.91 - 0.90| = 0.99     → +0.99
    #   valence: 0.75 × (1.0 - |0.48 - 0.48|)   → +0.75   [perfect match]
    #   danceability: 0.50 × (1.0 - |0.66-0.65|)→ +0.50   [near-perfect]
    #                                               ──────
    #                                    TOTAL      5.74 / 5.75
    #
    # The genre+mood bonuses alone contribute 3.50 / 5.75 = 60.9 % of the max score.
    # Storm Runner is the ONLY song in the 18-song catalog with both genre="rock" and
    # mood="intense", so it has an unassailable lead — no other song can bridge that
    # 3.5-point categorical gap through numeric similarity alone (max numeric = 2.25).
    #
    # Intuition check: does the ranking "feel right"?
    #   #1 Storm Runner  ✓  Heavy, fast (152 BPM), low acousticness — feels correct.
    #   #2 Gym Hero      ✗  A pop gym track at #2 feels wrong for a "deep rock" fan.
    #                       It only wins because mood="intense" fires (+1.5) and its
    #                       energy (0.93) is numerically close.  A real rock listener
    #                       would expect Iron Collapse (metal) here, not pop.
    #   #4 Iron Collapse ✗  A metal track ranks BELOW Night Drive Loop (synthwave).
    #                       Why? Night Drive Loop has better valence (0.49 vs 0.22 vs
    #                       target 0.48) and better danceability (0.73 vs 0.45 vs
    #                       target 0.65), so it wins on those two numeric axes even
    #                       though intuitively "metal" is closer to "rock" than
    #                       "synthwave" ever could be.  The system has no genre-family
    #                       concept, so metal ≈ synthwave ≈ folk once both miss genre.
    #
    # Root cause: categorical bonuses dominate (60 % of max).  With only one rock
    # song, positions #2-#5 are decided by numeric similarity alone — and valence +
    # danceability proximity can accidentally promote synthwave over metal.
    print_recommendations(
        label="Deep Intense Rock (rock / intense)",
        prefs={
            "genre": "rock",
            "mood": "intense",
            "target_energy": 0.90,
            "target_valence": 0.48,
            "target_danceability": 0.65,
            "target_acousticness": 0.10,
            "likes_acoustic": False,
        },
    )

    # =========================================================
    # ADVERSARIAL / EDGE-CASE PROFILES
    # Designed to stress-test scoring logic and expose weaknesses
    # =========================================================

    # --- Adversarial Profile 1: Conflicted Listener ---
    # High energy (0.9) paired with sad mood — these two signals are in tension.
    # Real-world meaning: thinks they want sad music but the numeric targets
    # all point to high-energy tracks.  The mood bonus (+1.5) will fight the
    # energy similarity term.  Only "Empty Glass" matches mood:sad, yet its
    # energy (0.38) is far from 0.9, so the mood bonus may not save it.
    print_recommendations(
        label="[ADVERSARIAL] Conflicted Listener (metal / sad, energy=0.9)",
        prefs={
            "genre": "metal",
            "mood": "sad",
            "target_energy": 0.90,
            "target_valence": 0.20,
            "target_danceability": 0.45,
            "target_acousticness": 0.10,
            "likes_acoustic": False,
        },
    )

    # --- Adversarial Profile 2: Genre Desert ---
    # Requests "country" — a genre that does NOT exist in the 18-song catalog.
    # No song will ever earn the +2.0 genre bonus; the system must fall back
    # entirely on mood + numerical similarity.  Exposes the catalog skew bias.
    print_recommendations(
        label="[ADVERSARIAL] Genre Desert (country / nostalgic)",
        prefs={
            "genre": "country",
            "mood": "nostalgic",
            "target_energy": 0.35,
            "target_valence": 0.62,
            "target_danceability": 0.50,
            "target_acousticness": 0.88,
            "likes_acoustic": True,
        },
    )

    # --- Adversarial Profile 3: All-Zeros Extremist ---
    # Every numeric target is 0.0 — an unreachable extreme.
    # Scores will be entirely driven by categorical matches and how close each
    # song is to silence-level energy/valence/danceability.
    # Exposes whether the math produces negative or nonsensical scores.
    print_recommendations(
        label="[ADVERSARIAL] All-Zeros Extremist (classical / melancholic)",
        prefs={
            "genre": "classical",
            "mood": "melancholic",
            "target_energy": 0.0,
            "target_valence": 0.0,
            "target_danceability": 0.0,
            "target_acousticness": 0.0,
            "likes_acoustic": True,
        },
    )


if __name__ == "__main__":
    main()
