from nba_api.live.nba.endpoints import scoreboard
import json

class Stats:
    def getMostRecentGameSummary():
        games_list = scoreboard.ScoreBoard()

        games = games_list.get_dict()["scoreboard"]["games"]
        warriors_game = {}

        for game in games:
            gamecode = game["gameCode"]
            if "GSW" in gamecode:
                warriors_game = game

        if not warriors_game:
            return "There isn't a warriors game today. Unfortunately I can only get warriors games on the same day right now."
        
        else:
            hometeam = warriors_game["homeTeam"]
            hometeam_name = hometeam["teamName"]
            hometeam_score = hometeam["score"]

            awayteam = warriors_game["awayTeam"]
            awayteam_name = awayteam["teamName"]
            awayteam_score = awayteam["score"]

            game_period = warriors_game["period"]
            game_clock = warriors_game["gameClock"]
            game_status = warriors_game["gameStatusText"]

            period_endings = ["st", "nd", "rd", "th"]
            game_period = str(game_period).join(period_endings[int(game_period) - 1])

            message = ""

            if "Final" not in game_status:
                message = message + f"There's {game_clock} left in the {game_period} quarter.\n"
            
            message = message + f"{hometeam_name} {hometeam_score}-{awayteam_score} {awayteam_name}"

            return message

            # print(json.dumps(warriors_game, indent=4))
            # print(json.dumps(games, indent=4))