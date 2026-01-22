"""
Seed data for Pink Floyd songs database.

This module contains curated data for 28 iconic Pink Floyd songs across their
most famous albums, with mood classifications and lyrics snippets.
"""

from typing import List, Dict, Any


PINK_FLOYD_SONGS: List[Dict[str, Any]] = [
    # The Dark Side of the Moon (1973)
    {
        "title": "Time",
        "album": "The Dark Side of the Moon",
        "year": 1973,
        "lyrics": "Ticking away the moments that make up a dull day\nYou fritter and waste the hours in an offhand way\nKicking around on a piece of ground in your home town\nWaiting for someone or something to show you the way",
        "mood": "melancholic",
        "duration_seconds": 413,
        "track_number": 4,
    },
    {
        "title": "Money",
        "album": "The Dark Side of the Moon",
        "year": 1973,
        "lyrics": "Money, get away\nGet a good job with more pay and you're okay\nMoney, it's a gas\nGrab that cash with both hands and make a stash",
        "mood": "energetic",
        "duration_seconds": 382,
        "track_number": 6,
    },
    {
        "title": "Us and Them",
        "album": "The Dark Side of the Moon",
        "year": 1973,
        "lyrics": "Us and them\nAnd after all we're only ordinary men\nMe and you\nGod only knows it's not what we would choose to do",
        "mood": "melancholic",
        "duration_seconds": 467,
        "track_number": 7,
    },
    {
        "title": "Brain Damage",
        "album": "The Dark Side of the Moon",
        "year": 1973,
        "lyrics": "The lunatic is on the grass\nThe lunatic is on the grass\nRemembering games and daisy chains and laughs\nGot to keep the loonies on the path",
        "mood": "psychedelic",
        "duration_seconds": 228,
        "track_number": 9,
    },
    {
        "title": "Eclipse",
        "album": "The Dark Side of the Moon",
        "year": 1973,
        "lyrics": "All that you touch and all that you see\nAll that you taste, all you feel\nAnd all that you love and all that you hate\nAll you distrust, all you save",
        "mood": "progressive",
        "duration_seconds": 123,
        "track_number": 10,
    },
    # The Wall (1979)
    {
        "title": "Comfortably Numb",
        "album": "The Wall",
        "year": 1979,
        "lyrics": "Hello, is there anybody in there?\nJust nod if you can hear me\nIs there anyone home?\nCome on now, I hear you're feeling down",
        "mood": "melancholic",
        "duration_seconds": 382,
        "track_number": 6,
    },
    {
        "title": "Another Brick in the Wall (Part 2)",
        "album": "The Wall",
        "year": 1979,
        "lyrics": "We don't need no education\nWe don't need no thought control\nNo dark sarcasm in the classroom\nTeachers leave them kids alone",
        "mood": "energetic",
        "duration_seconds": 238,
        "track_number": 3,
    },
    {
        "title": "Hey You",
        "album": "The Wall",
        "year": 1979,
        "lyrics": "Hey you, out there in the cold\nGetting lonely, getting old\nCan you feel me?\nHey you, standing in the aisles",
        "mood": "melancholic",
        "duration_seconds": 284,
        "track_number": 1,
    },
    {
        "title": "Run Like Hell",
        "album": "The Wall",
        "year": 1979,
        "lyrics": "Run, run, run, run, run, run, run, run\nYou better make your face up in\nYour favorite disguise\nWith your button down lips and your roller blind eyes",
        "mood": "energetic",
        "duration_seconds": 258,
        "track_number": 3,
    },
    {
        "title": "The Trial",
        "album": "The Wall",
        "year": 1979,
        "lyrics": "Good morning, the worm, your honor\nThe crown will plainly show\nThe prisoner who now stands before you\nWas caught red-handed showing feelings",
        "mood": "dark",
        "duration_seconds": 313,
        "track_number": 5,
    },
    # Wish You Were Here (1975)
    {
        "title": "Shine On You Crazy Diamond (Parts I-V)",
        "album": "Wish You Were Here",
        "year": 1975,
        "lyrics": "Remember when you were young, you shone like the sun\nShine on you crazy diamond\nNow there's a look in your eyes, like black holes in the sky",
        "mood": "progressive",
        "duration_seconds": 810,
        "track_number": 1,
    },
    {
        "title": "Wish You Were Here",
        "album": "Wish You Were Here",
        "year": 1975,
        "lyrics": "So, so you think you can tell\nHeaven from hell, blue skies from pain\nCan you tell a green field from a cold steel rail?\nA smile from a veil? Do you think you can tell?",
        "mood": "melancholic",
        "duration_seconds": 334,
        "track_number": 5,
    },
    {
        "title": "Welcome to the Machine",
        "album": "Wish You Were Here",
        "year": 1975,
        "lyrics": "Welcome my son, welcome to the machine\nWhere have you been? It's alright we know where you've been\nYou've been in the pipeline, filling in time",
        "mood": "dark",
        "duration_seconds": 467,
        "track_number": 2,
    },
    # Animals (1977)
    {
        "title": "Dogs",
        "album": "Animals",
        "year": 1977,
        "lyrics": "You gotta be crazy, you gotta have a real need\nYou gotta sleep on your toes, and when you're on the street\nYou gotta be able to pick out the easy meat with your eyes closed",
        "mood": "progressive",
        "duration_seconds": 1025,
        "track_number": 2,
    },
    {
        "title": "Pigs (Three Different Ones)",
        "album": "Animals",
        "year": 1977,
        "lyrics": "Big man, pig man, ha ha, charade you are\nYou well heeled big wheel, ha ha, charade you are\nAnd when your hand is on your heart\nYou're nearly a good laugh, almost a joker",
        "mood": "dark",
        "duration_seconds": 671,
        "track_number": 3,
    },
    {
        "title": "Sheep",
        "album": "Animals",
        "year": 1977,
        "lyrics": "Harmlessly passing your time in the grassland away\nOnly dimly aware of a certain unease in the air\nYou better watch out, there may be dogs about",
        "mood": "energetic",
        "duration_seconds": 625,
        "track_number": 4,
    },
    # Meddle (1971)
    {
        "title": "Echoes",
        "album": "Meddle",
        "year": 1971,
        "lyrics": "Overhead the albatross hangs motionless upon the air\nAnd deep beneath the rolling waves in labyrinths of coral caves\nThe echo of a distant time comes willowing across the sand",
        "mood": "progressive",
        "duration_seconds": 1435,
        "track_number": 6,
    },
    {
        "title": "One of These Days",
        "album": "Meddle",
        "year": 1971,
        "lyrics": "One of these days I'm going to cut you into little pieces",
        "mood": "psychedelic",
        "duration_seconds": 349,
        "track_number": 1,
    },
    # The Piper at the Gates of Dawn (1967)
    {
        "title": "Astronomy Domine",
        "album": "The Piper at the Gates of Dawn",
        "year": 1967,
        "lyrics": "Lime and limpid green, a second scene\nA fight between the blue you once knew\nFloating down, the sound resounds\nAround the icy waters underground",
        "mood": "psychedelic",
        "duration_seconds": 252,
        "track_number": 1,
    },
    {
        "title": "Interstellar Overdrive",
        "album": "The Piper at the Gates of Dawn",
        "year": 1967,
        "lyrics": "[Instrumental improvisation with spoken word segments]",
        "mood": "psychedelic",
        "duration_seconds": 585,
        "track_number": 7,
    },
    # More Albums
    {
        "title": "Mother",
        "album": "The Wall",
        "year": 1979,
        "lyrics": "Mother do you think they'll drop the bomb?\nMother do you think they'll like this song?\nMother do you think they'll try to break my balls?",
        "mood": "melancholic",
        "duration_seconds": 332,
        "track_number": 4,
    },
    {
        "title": "Young Lust",
        "album": "The Wall",
        "year": 1979,
        "lyrics": "I am just a new boy, a stranger in this town\nWhere are all the good times? Who's gonna show this stranger around?",
        "mood": "energetic",
        "duration_seconds": 195,
        "track_number": 9,
    },
    {
        "title": "Breathe",
        "album": "The Dark Side of the Moon",
        "year": 1973,
        "lyrics": "Breathe, breathe in the air\nDon't be afraid to care\nLeave but don't leave me\nLook around and choose your own ground",
        "mood": "melancholic",
        "duration_seconds": 163,
        "track_number": 2,
    },
    {
        "title": "The Great Gig in the Sky",
        "album": "The Dark Side of the Moon",
        "year": 1973,
        "lyrics": "[Primarily vocal improvisation by Clare Torry]",
        "mood": "progressive",
        "duration_seconds": 285,
        "track_number": 5,
    },
    {
        "title": "Have a Cigar",
        "album": "Wish You Were Here",
        "year": 1975,
        "lyrics": "Come in here, dear boy, have a cigar\nYou're gonna go far, you're gonna fly high\nYou're never gonna die, you're gonna make it if you try",
        "mood": "energetic",
        "duration_seconds": 305,
        "track_number": 3,
    },
    {
        "title": "Shine On You Crazy Diamond (Parts VI-IX)",
        "album": "Wish You Were Here",
        "year": 1975,
        "lyrics": "Nobody knows where you are, how near or how far\nShine on you crazy diamond\nPile on many more layers and I'll be joining you there",
        "mood": "progressive",
        "duration_seconds": 746,
        "track_number": 6,
    },
    {
        "title": "Set the Controls for the Heart of the Sun",
        "album": "A Saucerful of Secrets",
        "year": 1968,
        "lyrics": "Little by little the night turns around\nCounting the leaves which tremble at dawn\nLotuses lean on each other in yearning\nUnder the eaves the swallow is resting",
        "mood": "psychedelic",
        "duration_seconds": 327,
        "track_number": 3,
    },
    {
        "title": "Careful with That Axe, Eugene",
        "album": "Ummagumma",
        "year": 1969,
        "lyrics": "[Mostly instrumental with screaming vocals]",
        "mood": "dark",
        "duration_seconds": 531,
        "track_number": 2,
    },
]


def get_all_songs() -> List[Dict[str, Any]]:
    """Get all Pink Floyd songs data."""
    return PINK_FLOYD_SONGS


def get_songs_by_mood(mood: str) -> List[Dict[str, Any]]:
    """Get songs filtered by mood."""
    return [song for song in PINK_FLOYD_SONGS if song["mood"].lower() == mood.lower()]


def get_songs_by_album(album: str) -> List[Dict[str, Any]]:
    """Get songs filtered by album."""
    return [
        song for song in PINK_FLOYD_SONGS
        if album.lower() in song["album"].lower()
    ]


def get_songs_by_year(year: int) -> List[Dict[str, Any]]:
    """Get songs filtered by year."""
    return [song for song in PINK_FLOYD_SONGS if song["year"] == year]
