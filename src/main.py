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

    # --- Profile 2: Pop / happy listener ---
    print_recommendations(
        label="Upbeat Pop (pop / happy)",
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


if __name__ == "__main__":
    main()
