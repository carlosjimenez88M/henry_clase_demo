"""
Script to initialize and seed the Pink Floyd songs database.

Usage:
    python scripts/setup_database.py [--force]

Options:
    --force: Force recreation of database (will delete existing data)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.database.db_manager import DatabaseManager


def main():
    """Main function to setup database."""
    force_recreate = "--force" in sys.argv

    if force_recreate:
        print("  Force recreate mode: existing database will be deleted")
        response = input("Are you sure? (yes/no): ")
        if response.lower() != "yes":
            print("Aborted.")
            return

    print(f" Database path: {config.database_path}")

    # Initialize database manager
    db_manager = DatabaseManager(config.database_path)

    # Initialize and seed database
    db_manager.initialize_database(force_recreate=force_recreate)

    # Display statistics
    print("\n Database Statistics:")
    stats = db_manager.get_mood_statistics()
    for mood, count in sorted(stats.items()):
        print(f"   {mood}: {count} songs")

    # Display sample songs
    print("\n Sample Songs:")
    sample_songs = db_manager.get_all_songs(limit=5)
    for song in sample_songs:
        print(f"   €¢ {song.title} ({song.album}, {song.year}) - Mood: {song.mood}")

    print("\n Database setup complete!")


if __name__ == "__main__":
    main()
