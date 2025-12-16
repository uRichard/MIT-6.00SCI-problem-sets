
import csv
"""Data sources: goal.com Laliga
   Premier: Matchday google
"""
class MatchDay:
    """Models a football match on a given day."""
    def __init__(self,day, home_team, away_team, 
                home_team_score,away_team_score,
                half_time_home_goals = 0, half_time_away_goals =0) -> None:
        """Constructs a matchday object.
        day: The day of the Match, String.
        home_team: The team playing at home, String.
        away_team: The visiting team, String.
        home_team_score: The score of the home team, integer.
        away_team_score: The score of the visiting team, integer
        """
        self.day = day
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.half_time_home_goals = half_time_home_goals
        self.half_time_away_goals = half_time_away_goals

    def get_home_team(self):
        """
        returns the home team.
        return: home team, String
        """
        return self.home_team 

    def get_away_team(self):
        """
        returns the visiting team. 
        return: away team, String.
        """
        return self.away_team 

    def __str__(self) -> str:
        """returns String representation of a MatchDay object."""
        return self.home_team +" "+str(self.home_team_score) +" : "+ " "+ str(self.away_team)+" "+self.away_team_score   

class League:
    """Models a single league, e.g La Liga""" 
    def __init__(self) -> None:
        """
        Constructs a league object.
        league_matches: A dictionary that maps match object to each other.
        """
        self.league_matches = {}

    def add_league_match(self, league_match):
        """Adds a match to the league. Assume each match object is unique.
           league_match: The match. MatchDay object.
        """             
        self.league_matches[league_match] = league_match

    def get_league_matches(self):
        """returns all the matches in the league."""
        for key in self.league_matches:
            yield self.league_matches[key]

    def get_league_teams(self):
        """returns dict of numbers mapped to each team in a league.
           Will be used in menu selection.
           return: dict. e,g {1:Liverpool, 2:Arsenal,3:Everton}
        """
        temp_teams = []
        for key in self.league_matches:
            match_day = self.league_matches[key]
            home_team= match_day.get_home_team()
            visiting_team = match_day.get_away_team()
            if not home_team in temp_teams:
                temp_teams.append(home_team)
            if not visiting_team in temp_teams:
                temp_teams.append(visiting_team) 

        teams = {}
        for index in range(len(temp_teams)):
            teams[index + 1] = temp_teams[index]
        return teams

    def computeSta(self, proc, filt):
        """A helper method for computing statistics. e.g wins,draws,losses etc.
           proc: A procedure.
           filt: A filter.
        """
        return [proc(match_day) for match_day in self.league_matches.values() if filt(match_day)]

    def compute_home_wins(self,team_name):
        """Computes and returns all the games the team has won at home.
        team_name: The name of the team, String.
        return: list e.g if arsenal is home team["Arsenal", "ManU", (2,0)]
        test: works on dummy data
        """
        wins = self.computeSta(
            lambda x:[x.day,x.home_team, x.away_team,( x.home_team_score, x.away_team_score)], lambda y: y.home_team == team_name and y.home_team_score > y.away_team_score)
        return wins 

    def compute_home_losses(self, team_name):
        """Computes and returns the matches a team loses while playing away.
        team_name: The name of the team, String
        return: list of matches and results.
        e.g ["Arsenal", "Liverpool", (1,2)] for Arsenal 1: 2 Liverpool
        tested: worked
        """
        losses= self.computeSta(
            lambda x:[x.day,x.home_team, x.away_team,( x.home_team_score, x.away_team_score)], lambda y: y.home_team == team_name and y.home_team_score < y.away_team_score)
        return losses

    def compute_away_wins(self, team_name):
        """Computes and returns the games a team wins away.
        tested: works
        """

        wins_away = self.computeSta(lambda y: [y.day,y.home_team, y.away_team, (y.home_team_score, y.away_team_score)], lambda x: x.away_team == team_name and x.away_team_score > x.home_team_score)
        return wins_away

    def compute_away_losses(self, team_name):
        """Computes and returns games a team has LOST away i.e away games
        tested: it works
        """
        losses_away = self.computeSta(lambda y: [y.day,y.home_team, y.away_team, (y.home_team_score, y.away_team_score)], 
                             lambda x: x.away_team == team_name and x.away_team_score < x.home_team_score )
        return losses_away

    def computes_games_played(self, team_name,match_number):
        """Computes and returns all last 4 games the games played with results.
        team_name: The name of the team, String.
        match_number: The match number, Integer. e.g 3
        ruturn: list of lists e.g [["Away","day10",2,3], ...]
        tested: It works
        """
        played = self.computeSta(lambda x:[int(x.day[3:]),x.day,x.home_team, x.away_team,("Result:",x.home_team_score, x.away_team_score)], 
                    lambda y: y.home_team == team_name or y.away_team == team_name)
    
        results = []
        
        for var in played:
            #print("Output", var[0])
            if var[0] >= match_number:
                results.append(var)
            
        return results

    def compute_goals_conceded(self,team_name):
        """Computes and returns matches where a team conceded goals conceded
        tested: it works.
        returns list: Games where team has conceded a goal.
        This tells you how good the team is when compared to ther teams that concede alot.
        """
        goals_conceded_at_home = self.computeSta(lambda y: ["At Home",y.day,y.away_team_score],
                                    lambda x: x.home_team == team_name and x.away_team_score > 0)  
    
        goals_conceded_away = self.computeSta(lambda y: ["Away",y.day,y.home_team_score],
                                                lambda x: x.away_team == team_name and x.home_team_score > 0)
        results = goals_conceded_at_home + goals_conceded_away
        return results

    def compute_goals_scored(self, team_name):
        """Computes and returns goals scored, either at home or away.
        team_name:The name of the team, String.
        note:x or y are MatchDay objects.
        tested: works
        """
        #goals scored at home.
        goals_scored_at_home = self.computeSta(lambda y: ["At home",y.day,y.home_team_score],
                                    lambda x: x.home_team == team_name and x.home_team_score > 0)  
        #goals scored away.
        goals_scored_away = self.computeSta(lambda y: ["Away",y.day,y.away_team_score],
                                                lambda x: x.away_team == team_name and x.away_team_score > 0)
        results = goals_scored_at_home + goals_scored_away
        return results

    

    def compute_draw_matches(self,team_name):
        """When home and away team have equal golas"""
        drawsHome= self.computeSta(lambda y: ["At home",y.day,y.home_team_score],
                                    lambda x: x.home_team == team_name and x.home_team_score == x.away_team_score) 
        
        draws_away = self.computeSta(lambda y: ["Away",y.day,y.away_team_score],
                                                lambda x: x.away_team == team_name and x.away_team_score == x.home_team_score)
        return draws_away + drawsHome
        
    def compute_matches_under_two_goals(self, team):
        """Computes and returns matches with score under 2 goals."""
        pass

    def get_total_home_goals_scored(self,team_name,match_number):
        """Computes the total goals scored at home in last 4 games
        team_name: The team name, String.
        match_number:The match number.
        """

        #goals scored at home.
        goals_scored_at_home = self.computeSta(lambda y: ["At home",y.day,y.home_team_score],
                            lambda x: (x.home_team == team_name and x.home_team_score > 0) and (int(x.day[3:]) >= match_number))  
        sum = 0
        for var in goals_scored_at_home:
            sum = sum + var[2]
        return sum

    def get_total_away_goals_scored(self,team_name,match_number):
        """Computes the total goals scored away in last 4 games.
        team_name: The name of the team, String.
        match_number: The match number, Integer.
        return: Integer.
        """
        goals_scored_at_away = self.computeSta(lambda y: ["At Away",y.day,y.away_team_score],
                            lambda x: (x.away_team == team_name and x.away_team_score > 0) and (int(x.day[3:]) >= match_number))  
        sum = 0
        for var in goals_scored_at_away:
            sum = sum + var[2]
        return sum 

    def get_total_home_goals_conceded(self,team_name,match_number):
        """Computes and returns the goals conceded by a team at home.
        team_name:The name of the team, String.
        match_number: The match number, Integer.
        return: Integer
        """
        goals_conceded_at_home = self.computeSta(lambda y: ["At Home",y.day,y.away_team_score],
                                    lambda x: x.home_team == team_name and x.away_team_score > 0 and  (int(x.day[3:]) >= match_number))

        sum = 0
        for var in goals_conceded_at_home:
            sum = sum + var[2]
        return sum 

    def get_total_away_goals_conceded(self,team_name,match_number):
        """Computes and returns the total goals conceded by a team
        playing away in last 4 games.
        team_name: The team name, String.
        match_number: The match_number
        Works.
        buggy
        """
        goals_conceded_away = self.computeSta(lambda y: ["Away",y.day, y.home_team_score],
                                                lambda x: x.away_team == team_name and x.home_team_score > 0 and (int(x.day[3:]) >= match_number))                                       
        sum = 0
        for var in goals_conceded_away:
            #print("Output",var)
            sum = sum + var[2]
        return sum 
    
    
     
   
      

def get_dumy_Data():
    """Loads dumy data manualy created from objects. NOT USED. For testing
    league: league object
    """
    league = League()
    g1 = MatchDay("day1", "Ipswich", "Liverpool", 0, 2)
    g2 = MatchDay("day2", "Arsenal", "Wolves", 2, 4)
    g3 = MatchDay("day3", "Ipswich", "Liverpool",0,2)
    g4 = MatchDay("day4", "Arsenal", "Leicester", 0, 2)
    g5 = MatchDay("day5", "Southampton", "Arsenal", 4, 1)
    g6 = MatchDay("day6", "Wolves", "Liverpool", 0, 1)
    g7 = MatchDay("day7", "Man Utd", "Arsenal", 2, 5)
    g8 = MatchDay("day8","Man UTD", "Fulham", 0, 1)
    
    league.add_league_match(g1)
    league.add_league_match(g2)
    league.add_league_match(g3)
    league.add_league_match(g4)
    league.add_league_match(g5)
    league.add_league_match(g6)
    league.add_league_match(g7)
    league.add_league_match(g8)
    
    return league


def getData(filename,reader):
    """loads data from file and adds to league object.
    return: league object.
    """
    league = League()
    for row in reader:
        m_day = row['matchday'] 
        home_team = row['homeTeam']
        away_team = row['awayTeam']
        home_team_score = row['homeTeamScore']
        away_team_score = row['awayTeamScore']
        #half_time_home_goals = row['halfTime_home_team_goals']
        #half_time_away_goals = row['halfTime_away_team_goals']

        #print(m_day,home_team_score, ":",away_team_score, away_team )
        #print("Away Team Score: ",away_team_score)
        
        home_team_score = int(home_team_score)
        away_team_score = int(away_team_score)
       # half_time_home_goals = int(half_time_home_goals)
        #half_time_away_goals = int(half_time_away_goals)
        
        match_day = MatchDay(m_day,home_team, away_team,
                            home_team_score, away_team_score,
                            )

        league.add_league_match(match_day)
        
    return league     
        

def menu(teams, league,match_number):
    """provides selection command
    teams: dictionary
    """
    print("\nMenu:")
    for team in teams:
        print(team, teams[team])
    
    home_team= int(input("Enter Number of Home Team: "))
    
    away_team = int(input("Enter Number of Away Team: "))
    #print(teams.keys())
    
    while True:
        
        if home_team == "q" or away_team == "q":
           print("exiting...")
           break
        elif home_team in teams.keys() and away_team in teams.keys():
           #showStatistics(teams[home_team], teams[away_team], league)
           #print("Goals scoresd: ",league.get_median_goals_scored())
           homeTeam = displaySta2(teams[home_team],league,match_number)
           awayTeam = displaySta2(teams[away_team],league,match_number)
           myBet = bet2(homeTeam,awayTeam)
           return myBet
           #break
 

def bet2(home_team, away_team):
    """We compare two teams. i.e home team and away team.
    home_team: a tuple with hometeam, goals scored and goals conceded in last 5 matches. e.g ("Arsenal",15,6)
    away_team: Tuple with awayteam, goals scored and goals conceded. e.g ("Burnly",8,9)
    Lets use Ratios
    """
    winThreshold_ratio = 0.3
    both_teams_to_score_ratio= 0.8
    goals_scored_threshold = 5
    bet = " "
    
    home_deno = 0
    away_deno = 0
    #comparing ratio of conceded goals to scored goals.
    
    if home_team[1] == 0 or away_team[1] == 0:
       home_deno= home_deno + 1
       away_deno = away_deno + 1 
    else:
         home_deno = home_deno + home_team[1] 
         away_deno = away_deno + away_team[1]                       
                
    home_team_ratio = home_team[2] / home_deno
    away_team_ratio = away_team[2] / away_deno
    #Compare goals conceded.
    if home_team_ratio <= winThreshold_ratio:
        if home_team_ratio <= away_team_ratio:
            bet = bet +home_team[0] +" to WIN!! RE-EXAMINE PLEASE."
        else:
            bet = bet + "Do Not Bet On this Match. Ratio NOT less than 0.3."
        
    elif away_team_ratio <= winThreshold_ratio:
        if away_team_ratio <= home_team_ratio:
            bet = bet + away_team[0]+ " to WIN!! RE-EXAMINE!!"
        else:
            bet = bet + "Do Not Bet On this Match. Ratio not less than 0.3."    
            
    elif away_team_ratio >= both_teams_to_score_ratio and home_team_ratio >= both_teams_to_score_ratio:
        if home_team[1] >= goals_scored_threshold or away_team[1] >= goals_scored_threshold:
            bet = bet+" Both Teams to Score!!"
        else:
            bet = bet + "Do Not Bet On this Match. Goal Threshold low!"    
   
    else:
        bet = bet+"DO NOT BET THIS  MATCH. Find other Matches Please."
        
    return bet          
def bet(home_team, away_team):
    """We compare two teams. i.e home team and away team.
    home_team: a tuple with hometeam, goals scored and goals conceded in last 5 matches. e.g ("Arsenal",15,6)
    away_team: Tuple with awayteam, goals scored and goals conceded. e.g ("Burnly",8,9)
    """
    bet = ""
    #comparing goals conceded:
    goals_conceded = abs(home_team[2] - away_team[2])
    
    #Compare goals conceded.
    if home_team[2] >= 7 and away_team[2] > 7:
        #compare goals scored.
        if home_team[1] >= 6 and away_team[1] >= 6:
            
            bet = bet +home_team[0]+" Vs "+away_team[0]+" Both teams to SCORE, Highly likey."
        else:
            print("Avoid This BET.!!!")
    elif goals_conceded >=7:
         homeTeamGoals = home_team[1]
         awayTeamGoals = away_team[1]
         if homeTeamGoals >= 7 and awayTeamGoals <=7:
             bet=bet+home_team[0] + "To WIN. RE- EXAMINE Please!! WINS are RISKY"
         elif awayTeamGoals >=7 and awayTeamGoals <=7:
             bet = bet + away_team[0] + "To Win. RE-EXAMINE Please. WINS HAVE MORE RISK"
    else:
        bet = bet+"Avoid betting on this Match. Find other Matches Please."
    return bet        
            
        
        
def displaySta2(team_name,league,match_number):
    """Displays statistics of a team in last four matches. Useful in finding a pattern on how team performs.
       team_name: The name of the team, String.
       league: The League object.
       match_number: The match number, Integer. E.g day13, match number is 13
    """
    
    total_goals_scored_at_home = league.get_total_home_goals_scored(team_name,match_number)
    total_goals_scored_at_away = league.get_total_away_goals_scored(team_name,match_number)
    total_goals_scored = total_goals_scored_at_home + total_goals_scored_at_away
    
    total_goals_conceded_at_home = league.get_total_home_goals_conceded(team_name,match_number)
    total_goals_conceded_at_away = league.get_total_away_goals_conceded(team_name,match_number)
    total_goals_conceded = total_goals_conceded_at_home + total_goals_conceded_at_away
    
    games_played = league.computes_games_played(team_name,match_number)

    print("\nStatistics of last Four Matches: ", team_name, sep="")
    print("Goals scored at home: ",total_goals_scored_at_home)
    print("Goals scored Away: ",total_goals_scored_at_away)
    print("Total Goals Scored: ",total_goals_scored)
    
    print("\nGoals conceded at home: ",total_goals_conceded_at_home)
    print("Goals conceded Away: ",total_goals_conceded_at_away)
    print("Total Goals Conceded: ",total_goals_conceded)
    
    print("Summary of Last "+str(match_number)+" Matches of ",team_name+":")
    for result in games_played:
        print(result)
    
    return (team_name, total_goals_scored,total_goals_conceded)

def displaySta(team_name,league,match_number):
    """Displays statistics of a team in last four matches. Useful in finding a pattern on how team performs.
       team_name: The name of the team, String.
       league: The League object.
       match_number: The match number, Integer. E.g day13, match number is 13
    """
    
    total_goals_scored_at_home = league.get_total_home_goals_scored(team_name,match_number)
    total_goals_scored_at_away = league.get_total_away_goals_scored(team_name,match_number)
    total_goals_conceded_at_home = league.get_total_home_goals_conceded(team_name,match_number)
    total_goals_conceded_at_away = league.get_total_away_goals_conceded(team_name,match_number)
    
    games_played = league.computes_games_played(team_name,match_number)
    print("\nStatistics of last Four Matches: ", team_name, sep="")
    print("Goals scored at home: ",total_goals_scored_at_home)
    print("Goals scored Away: ",total_goals_scored_at_away)
    print("Goals conceded at home: ",total_goals_conceded_at_home)
    print("Goals conceded Away: ",total_goals_conceded_at_away)
    print("\nSummary of Last four games:")
    for result in games_played:
        print(result)
    
    print("\nBet Tip:\n A team that has CONCEDED LESS GOALS in LAST 4 GAMES is STRONGER than a team that has CONCEDED MORE GOALS even though it has scored more goals. The LESS Goals a team CONCEDES the STRONGER it is.\nWARNING:\nDo not consider the goals scored. If two teams have CONCEDED the SAME NUMBER OF GOALS CONSIDER a DRAW or Dont bet on them.\nBet for the Stronger team to WIN, Numbers do not LIE.\nIgnore the home or Away. Just consider goals a team has conceded. Ignore exceptions..That is the pattern. Some big teams STAGE Losses, They do not want us to figure out the pattern. Especially 4 historical big 4 teams. e.g Arsenal,Chealsea, Sometimes they stage losses.\nIf odd is small for a win choose over 1.5 goals, its less risky")
    
 

def main():
    """league = get_dumy_Data() testing
    goals_in = league.compute_goals_conceded("Arsenal")
    #away_losses = league.compute_away_losses("Arsenal")
    #print("Arsenal Away Wins: ",away_wins)
    print("\nArsenal Goals Conceded: ", goals_in)
    
    How To: to analyse premiership data, use ndagano_EPL.csv
    To change match number, tinker the match_number variable here.
    DATA source csv files: football-data.co.uk  
    Updating data: goal.com, livescore.com, search, type England competitions.
    
    """
    #ENGLAND
    #filename="England_EPL_Season25_26.csv" # English Premier League.
    #filename="ENG_Championship.csv" # English Championship.
    #filename="ENG_National_League.csv" # England National League.
    #filename="ENG_League1.csv" # England League one.
    #filename="ENG_League2.csv" # England League Two. 
    #filename="ENG_National_LeagueNorth.csv" # England National League NORTH.

    #FRANCE
    #filename="FRANCE_league1_Season25_26.csv" # FRENCH LEAGUE 1.
    #filename="FRANCE_DIVISION2_NEW.csv" # FRENCH DIVISION 1.

    #GERMANY
    #filename="Germany_Bundesliga_Season25_26.csv" # Germany Bundesliga.
    #filename="Germany_Division2.csv" #Germany Divion 2.

    #ITALY
    #filename="Italy_serieA_Season25_26.csv" #Italy Serie A.
    #filename="ITALY_SerieB.csv" Italy Serie B.

    #SPAIN f
    filename = "Spanish_Laliga_Season_25_26.csv" #SPAIN LA-LIGA

    reader = csv.DictReader(open(filename, 'r') ) # load data from file.
    league = getData(filename,reader) # loads data to memory
    teams = league.get_league_teams()
    
    match_number = 14
    
    # tracking matches from day10...modify to fit
    
    myBet = menu(teams, league,match_number)
    print("\nCOMPUTER PREDICTIONS:")
    print(myBet)


if __name__ == "__main__":
    main()