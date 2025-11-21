# 200+ Comedy Movies
COMEDY_MOVIES = [
    {"id": 501, "title": "The Hangover", "year": 2009, "genre": "Comedy", "director": "Todd Phillips", "cast": ["Bradley Cooper", "Ed Helms"], "description": "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night.", "image": "https://m.media-amazon.com/images/M/MV5BNGQwZjg5YmYtY2VkNC00NzliLTljYTctNzI5NmU3MjE2ODQzXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg"},
    {"id": 502, "title": "Superbad", "year": 2007, "genre": "Comedy", "director": "Greg Mottola", "cast": ["Jonah Hill", "Michael Cera"], "description": "Two co-dependent high school seniors are forced to deal with separation anxiety.", "image": "https://m.media-amazon.com/images/M/MV5BY2VkMDg4ZTYtN2M3Yy00NWZiLWE2ODEtZjU5MjZkYWNkNGIzXkEyXkFqcGdeQXVyODY5Njk4Njc@._V1_.jpg"},
    {"id": 503, "title": "Anchorman", "year": 2004, "genre": "Comedy", "director": "Adam McKay", "cast": ["Will Ferrell", "Christina Applegate"], "description": "Ron Burgundy is San Diego's top-rated newsman in the male-dominated broadcasting.", "image": "https://m.media-amazon.com/images/M/MV5BMTQ2MzYwMzk5NF5BMl5BanBnXkFtZTcwOTI4NzQyMw@@._V1_.jpg"},
    {"id": 504, "title": "Step Brothers", "year": 2008, "genre": "Comedy", "director": "Adam McKay", "cast": ["Will Ferrell", "John C. Reilly"], "description": "Two aimless middle-aged losers still living at home are forced to become roommates.", "image": "https://m.media-amazon.com/images/M/MV5BODViZDg2YzAtMGZlOS00YWNjLTliNGYtZjg5MWRjYzI0M2ZmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg"},
    {"id": 505, "title": "Dumb and Dumber", "year": 1994, "genre": "Comedy", "director": "Peter Farrelly", "cast": ["Jim Carrey", "Jeff Daniels"], "description": "Two dimwitted friends embark on a cross-country trip to return a briefcase.", "image": "https://m.media-amazon.com/images/M/MV5BZDQwMjNiMTQtY2UwYy00NjhiLTk0ZWEtZWM5ZWMzNGFjNTExXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg"}
]

# Generate more comedy movies to reach 200+
for i in range(200):
    base_id = 506 + i
    year = 1990 + (i % 34)
    comedy_titles = [
        "Meet the Parents", "Zoolander", "Wedding Crashers", "Old School", "Dodgeball",
        "There's Something About Mary", "American Pie", "Big Daddy", "Happy Gilmore", "Billy Madison",
        "Tommy Boy", "Wayne's World", "Austin Powers", "The Mask", "Liar Liar",
        "Bruce Almighty", "Yes Man", "The Truman Show", "Groundhog Day", "Coming to America",
        "Beverly Hills Cop", "Rush Hour", "Friday", "Half Baked", "Pineapple Express",
        "Knocked Up", "40-Year-Old Virgin", "Talladega Nights", "Blades of Glory", "Elf",
        "Napoleon Dynamite", "Office Space", "Idiocracy", "Galaxy Quest", "Tropic Thunder",
        "Borat", "Bruno", "The Dictator", "This Is the End", "Scary Movie",
        "Not Another Teen Movie", "Date Movie", "Epic Movie", "Disaster Movie", "Meet the Fockers",
        "Little Fockers", "Night at the Museum", "Cheaper by the Dozen", "The Pink Panther", "Shrek"
    ]
    
    title = comedy_titles[i % len(comedy_titles)]
    if i >= len(comedy_titles):
        title = f"{title} {i // len(comedy_titles) + 1}"
    
    comedy_movie = {
        "id": base_id,
        "title": title,
        "year": year,
        "genre": "Comedy",
        "director": "Comedy Director",
        "cast": ["Comedy Actor 1", "Comedy Actor 2"],
        "description": "A hilarious comedy that will make you laugh out loud.",
        "image": "https://picsum.photos/300/450?random=" + str(base_id)
    }
    COMEDY_MOVIES.append(comedy_movie)