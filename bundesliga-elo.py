import csv

mean_rating = 1500   # ø = 1500
K = 20               # K-factor

def rating_update(home_rating, away_rating, home_goals, away_goals):
    # Determine outcome of match
    if home_goals > away_goals:
        outcome = 1.0
    elif home_goals < away_goals:
        outcome = 0.0
    else:
        outcome = 0.5

    # Calculate expected scores using a standard formula for elo
    expected_home = 1.0 / (1 + 10 ** ((away_rating - home_rating) / 400.0))
    expected_away = 1.0 - expected_home

    # Update ratings
    new_home_rating = home_rating + K * (outcome - expected_home)
    new_away_rating = away_rating + K * ((1.0 - outcome) - expected_away)

    return new_home_rating, new_away_rating


def calculate_elo(csv_filename, mean_rating, K):
    team_ratings = {}
    # Read csv bundesliga database
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Go over each match, updating the teams ratings
        for row in reader:
            home_team = row["Home Team"]
            away_team = row["Away Team"]
            result = row["Result"]
            home_goals_str, away_goals_str = result.split("-")
            # Strip any surrounding whitespace and convert to integers
            home_goals = int(home_goals_str.strip())
            away_goals = int(away_goals_str.strip())

            # If teams are new, initialize them
            if home_team not in team_ratings:
                team_ratings[home_team] = 1500
            if away_team not in team_ratings:
                team_ratings[away_team] = 1500

            # Calculate the updated ratings
            new_home_rating, new_away_rating = rating_update(
                team_ratings[home_team],
                team_ratings[away_team],
                home_goals,
                away_goals
            )
            # Update ratings
            team_ratings[home_team] = new_home_rating
            team_ratings[away_team] = new_away_rating

    return team_ratings


if __name__ == "__main__":
    final_ratings = calculate_elo("bundesliga-23-24.csv", mean_rating, K)

    # Sort teams by rating
    sorted_ratings = sorted(
        final_ratings.items(),
        key=lambda item: item[1],
        reverse=True
        )

    # Calculate longest team name for formatting
    max_team_length = max(len(team) for team in final_ratings)

    # Print team names and their rounded ratings
    for team, rating in sorted_ratings:
        rating = round(rating)
        print(f" {team:<{max_team_length}}  {rating:>6}")
