from nba_api.live.nba.endpoints import scoreboard
import json

class Stats:
    # Returns the summary of the game
    def getMostRecentGameSummary():
        games_list = scoreboard.ScoreBoard()
        games = games_list.get_dict()["scoreboard"]["games"]
        warriors_game = {}

        for game in games:
            gamecode = game["gameCode"]
            if "GSW" in gamecode:
                warriors_game = game

        message = ""
        if not warriors_game:
            return Stats.noWarriorsGame()
        
        else:
            info = Stats.getInfo(warriors_game)

            if ":" in info["game_status"] and "ET" in info["game_status"]:
                return Stats.futureGame(info["hometeam_name"], info["hometeam_record"], info["awayteam_name"],
                                         info["awayteam_record"], info["game_status"])

            if "Final" not in info["game_status"]:
                message = message + Stats.getCurrentGame(info["game_clock"], info["game_period"])
            else:
                message = message + "The game has ended.\n"
            
            message = message + f'{info["hometeam_name"]} {info["hometeam_score"]}-{info["awayteam_score"]} {info["awayteam_name"]}'
            return message
        
    # Returns a string when there is no warriors game
    def noWarriorsGame():
        return "There isn't a warriors game today. Unfortunately I can only get warriors games on the same day right now."
    
    # Returns a summary of a future game
    def futureGame(hometeam_name, hometeam_record, awayteam_name, awayteam_record, game_status):
        return f"""Today's game:\n {hometeam_name} {hometeam_record} vs {awayteam_name} 
                    {awayteam_record} in {hometeam_name.split()[0]} at {game_status}"""
    
    # Returns a summary of the current game in progress
    def getCurrentGame(game_clock, game_period):
        return f"There's {game_clock} left in the {game_period} quarter.\n"
    
    # Returns a dictionary of info from the API
    def getInfo(warriors_game):
        hometeam = warriors_game["homeTeam"]
        hometeam_record = "(" + str(hometeam["wins"]) + "-" + str(hometeam["losses"]) + ")"
        hometeam_name = hometeam["teamCity"] + " " + hometeam["teamName"]
        hometeam_score = hometeam["score"]

        awayteam = warriors_game["awayTeam"]
        awayteam_record = "(" + str(awayteam["wins"]) + "-" + str(awayteam["losses"]) + ")"
        awayteam_name = awayteam["teamCity"] + " " + awayteam["teamName"]
        awayteam_score = awayteam["score"]

        game_period = warriors_game["period"]
        game_status = warriors_game["gameStatusText"]

        period_endings = ["st", "nd", "rd", "th"]
        game_period = str(game_period) + period_endings[int(game_period) - 1]
        game_clock = warriors_game["gameClock"][2:4] + ":" + warriors_game["gameClock"][5:7]

        info = {
            "hometeam_record": hometeam_record,
            "hometeam_name": hometeam_name,
            "hometeam_score": hometeam_score,
            "awayteam_record": awayteam_record,
            "awayteam_name": awayteam_name,
            "awayteam_score": awayteam_score,
            "game_period": game_period,
            "game_status": game_status,
            "game_clock": game_clock
        }

        return info
