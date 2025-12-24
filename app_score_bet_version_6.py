   
     
   
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
        """Adds a match object to the league object. Assume each match object is unique.
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
     
    def computes_games_played(self, team_name,match_number):
        """Computes and returns all last 4 games the games played with results.
        team_name: The name of the team, String.
        match_number: The match number, Integer. e.g 3
        ruturn: list of lists e.g [["Away","day10",2,3], ...]
        tested: It works
        """
        played = self.computeSta(lambda x:[int(x.day[3:]),x.day,x.home_team, x.away_team,x.home_team_score, x.away_team_score], 
                    lambda y: y.home_team == team_name or y.away_team == team_name)
    
        
        results = []
        for var in played:
            #print("Output", var[0])
            if var[0] >= match_number:
                results.append(var)
            
        return results

      
    def get_match_days(self):
        """
        Computes and returns match days.
        return: list
        """
        match_days = set()
        for match in self.league_matches:
            match_days.add(match.day)
        return match_days
        

    def get_single_match_day_goals(self,match_day):
        """Computes and returns the total goals in a single matchday.
        Now we can know goals in each match day.
        This will help us to set a better goal threshold we wanted.
        match_day: The match day number, integer.
        return: list. e.g[ ["matchday1",10],["matchday2",6]]. macthday1 has 10 goals.
        """
        goals_in_match_day = self.computeSta(lambda y: ["Matchday",y.day,y.home_team_score + y.away_team_score ],
                              lambda x: int(x.day[3:]) == match_day)
        results = []
        total = 0
        num_of_matches = 0
        for match in goals_in_match_day:
            num_of_matches = num_of_matches + 1
            total = total + match[2]
        results.append(("Number of Matches: ",num_of_matches,"Total Goals: match day "+str(match_day),total))
        
        return results
    
    def get_ALL_match_day_Goals(self):
        """ returns a list of each match day with its goals
           [[matchday1, 10],[matchday2,7]]
           We will use this method to compute average number of goals in league.
           Then we will compute goals scored per game.
           then we will derive our assumptions on goal threshold.
        """
          
        results = []
        match_days  = self.get_match_days()
        #print(match_days)
        for index in range(1,len(match_days) + 1):
            match_day_goals = self.get_single_match_day_goals(index)
            #print(match_day_goals)
            results.append(match_day_goals)
         
        return results
         
    def compute_goal_threshold(self):
        """Each league has some goal threshold.
           We need to compute that.
        """    
        #step1: compute average goals in all match days
        matches = self.get_ALL_match_day_Goals()
        total_goals = 0
        for m in matches:
            #total_goals = total_goals + m[0]m[-1]
            match_day = m[0]
            total_goals = total_goals + match_day[-1]
            #print(match_day[-1])
            #print(m[0])
        average_goals_in_all_matchdays = total_goals/len(matches)
        #num_of_teams = self.get_league_teams() #
        index  = matches[0]
        num_of_teams = index[0]
        #print("Index", num_of_teams[1])
        match_number = 5
        average_goals_in_five_matches = (average_goals_in_all_matchdays/num_of_teams[1])* match_number
        
        average_goals_in_five_matches = round(average_goals_in_five_matches)
        #goals_conceded = 3
        #goals_threshold_scored = average_goals_in_five_matches  - goals_conceded

        return average_goals_in_five_matches #goals_threshold_scored
         
    def get_total_home_goals_scored(self,team_name,match_number):
        """Computes the total goals scored at home in last 5 games
        team_name: The team name, String.
        match_number:The match number.
        Test: it works.
        """
        #goals scored at home.
        results = self.computes_games_played(team_name, match_number)
        
        sum = 0
        for var in results:
            if team_name == var[2]:
                goals = int(var[4])
                sum = sum + goals
        return sum

    def get_total_away_goals_scored(self,team_name,match_number):
        """Computes the total goals scored away in last 4 games.
        team_name: The name of the team, String.
        match_number: The match number, Integer.
        return: Integer.
        """
        results = self.computes_games_played(team_name, match_number)
        
        sum = 0
        for var in results:
            if team_name == var[3]:
                goals = int(var[5])
                sum = sum + goals
        return sum 

    def get_total_home_goals_conceded(self,team_name,match_number):
        """Computes and returns the goals conceded by a team at home.
        team_name:The name of the team, String.
        match_number: The match number, Integer.
        return: Integer
        """
        results = self.computes_games_played(team_name, match_number)
        
        sum = 0
        for var in results:
            if team_name == var[2]:
                sum = sum + int(var[5])
        return sum 

    def get_total_away_goals_conceded(self,team_name,match_number):
        """Computes and returns the total goals conceded by a team
        playing away in last 4 games.
        team_name: The team name, String.
        match_number: The match_number
        Works.
        buggy
        """
        results = self.computes_games_played(team_name, match_number)
        sum = 0
        for var in results:
            if team_name == var[3]:
                goals = var[4]
                sum = sum + goals
        return sum 
   
    def compute_goals_scored_goals_conceded(self,teams,match_number):
        """
        Computes the total goals scored and total goals conceded in last 5 matches
        for each team in the league. This method will be used to grade each team.

        teams: A dictionary with elements team names e.g {1: "Arsenal",2:"ManU", 3: "Everton"}
        teams[key]: The name of the team, String. 
        league: The league object.
        match_number: The number for computing last 5 matches,integer.
        return: list. e.g [("Arsenal",5,9),("man U",7,9),...] 
        where index 0 is team name, index 1 is goals scored, index 2 is goals conceded.
        """
        results = []
        teams = teams.copy()
        for key in teams:
            goals_scored_at_home = self.get_total_home_goals_scored(teams[key],match_number)
            goals_scored_at_away = self.get_total_away_goals_scored(teams[key],match_number)
            total_goals_scored =   goals_scored_at_home + goals_scored_at_away
        
            goals_conceded_at_home = self.get_total_home_goals_conceded(teams[key],match_number)
            goals_conceded_at_away = self.get_total_away_goals_conceded(teams[key],match_number)
            total_goals_conceded =   goals_conceded_at_home + goals_conceded_at_away
            results.append((teams[key], total_goals_scored, total_goals_conceded))

        return results   

    def grade_team(self,team):
        """
        Grades a single team. 
        team: team, tuple. ("Arsenal",6,15) a total 6 goals conceded, 15 goals scored in last 5 matches.
        
        Best team:
        Win case1: team has scored morethan max goals in 5 matches and has conceded less than min threshold.
        Win case2:team has scored morethan 3/4 of goal threshold and conceded less than minimum.
        Win case3: has has scored more than average and conceded less than min goals.

        Average team:
        case 1: conceded between 1/2 and score 1/2 or more goals. good for both teams to score.


        Worst team:
        case 1:
        """
        #asummed_conceded_goals = 2 #assume the best team has conceded 3 goals
        goal_threshold = self.compute_goal_threshold() 
        #max_goal_thresholdoals_scored = goal_threshold - asummed_conceded_goals #goals in 5 match days.
        
       
        max_goal_thresholdoals_scored = self.compute_goal_threshold() 
        #max_goal_thresholdoals_scored = max_goal_thresholdoals_scored - asummed_conceded_goals
        #goal scoring range.
        near_max_goal_thresholdoals_scored = round( (3/4) * max_goal_thresholdoals_scored )
        average_goals_scored = round( (1/2) * max_goal_thresholdoals_scored )
        min_goalsoals_scored = round( (1/4) * max_goal_thresholdoals_scored )
        
        #goals conceded range.
        near_max_goal_thresholdoals_conceded = round( (3/4) * max_goal_thresholdoals_scored )
        average_goals_conceded = round( (1/2) * max_goal_thresholdoals_scored )
        min_goalsoals_conceded = round( (1/4) * goal_threshold)
        
        team_name = team[0]
        goals_scored = int(team[1])
        goals_conceded = int(team[2])

        grade = ""

        #case 1: best team. score morethan than max goals and concede less than minimum
        if (goals_scored >= max_goal_thresholdoals_scored and goals_conceded <= min_goalsoals_conceded) or (goals_scored >= near_max_goal_thresholdoals_scored and goals_conceded <= min_goalsoals_conceded):
            grade = grade + "A"

        #case 2: average teams. good for both teams to score.
        elif (goals_scored >= max_goal_thresholdoals_scored and goals_conceded >= average_goals_conceded) or (goals_scored >= near_max_goal_thresholdoals_scored and goals_conceded >= average_goals_conceded) or (goals_scored >= average_goals_scored and goals_conceded >= average_goals_conceded ):
            grade = grade + "B"
        
        #case 3: worst teams.
        elif (goals_scored <= min_goalsoals_scored and goals_conceded >= max_goal_thresholdoals_scored) or (goals_scored <= min_goalsoals_scored and goals_conceded >= near_max_goal_thresholdoals_conceded)or (goals_scored <= min_goalsoals_scored and goals_conceded >= average_goals_conceded):
            grade = grade + "C"
        
        else:
            grade = "UNGRADED"

        return (team_name, grade)  
        
    def grade_all_teams(self,match_number):
        """Grades each team in the league. {"A":["Fulham","Arsenal"],..}
        

        Best to win have a key of 1,
        Average teams have a key of 2
        Worst teams have a key of 3

        teams: dict. {1:"Liverpool", 2:"Everton"} from league.getteams()
        return a list of tuples. e.g [(),()]
        """
        results = { "A":[], "B":[], "C":[], "UNGRADED":[] }
        teams = self.get_league_teams()
        teams_data = self.compute_goals_scored_goals_conceded(teams,match_number)

        for team in teams_data:
            team_name = team[0]
            total_goals_scored = team[1]
            total_goals_conceded = team[2]
            grade = self.grade_team(team)
            print("Grade: Line 345:", grade)
            if grade[1] == "A":
                results["A"].append((grade[0], "best team to win a match"))
            elif grade[1] == "B":
                results["B"].append((grade[0],"average teams, score and concede. bothe teams to score bet"))
            elif grade[1] == "C":
                results["C"].append((grade[0],"Worst teams. concede alot score less"))       
            else:
                results["UNGRADED"].append((grade[0],"Ungraded. check why"))

            return results
    
    def both_teams_to_score(self,match_number):
        """
        Computes and returns teams which have conceded and scored more than
        the average total goals in 5 matches.
        These teams always score each other.
        teams: list. [("Arsenal",7,8),("Newcastle",7,9)] from 
        """
        max_goal_thresholdoal_threshold = self.compute_goal_threshold()
        
        average_total_goals = round( (1/2) * max_goal_thresholdoal_threshold)
        print("Average Goals: ",average_total_goals)
        teams = self.get_league_teams()
        teams_data = self.compute_goals_scored_goals_conceded(teams,match_number)

        results = []
        for result in teams_data:
            goals_scored = int(result[1])
            goals_conceded = int(result[2])
            if goals_scored >= average_total_goals and goals_conceded >= average_total_goals:
                results.append(result)

        return results

    def best_teams_to_win(self,match_number):
        """Collects the best teams in the league.
        These teams win the match.
        They conceded less than the minimum goals and score above maxima.
        """
        max_goal_thresholdoal_threshold = self.compute_goal_threshold()
        near_max_goal_thresholdoal_threshold =  round( (3/4) * max_goal_thresholdoal_threshold)
        average_total_goals = round( (1/2) * max_goal_thresholdoal_threshold)
        min_goalsoals_goal_threshold =  round( (1/4) * max_goal_thresholdoal_threshold)
        teams = self.get_league_teams()
        teams_data = self.compute_goals_scored_goals_conceded(teams,match_number)

        results = []
        for result in teams_data:
            goals_scored = int(result[1])
            goals_conceded = int(result[2])
            if (goals_conceded <= min_goalsoals_goal_threshold and goals_scored >= near_max_goal_thresholdoal_threshold) or (goals_conceded <= min_goalsoals_goal_threshold and goals_scored > average_total_goals):
                results.append(result)

        return results

    def second_best_teams(self, match_number):
        """Computes second best teams
          A team which has conceded less than the minimum goals
          and scored above the average goals. 
          Theses are winners too.
        """
        
        max_goal_thresholdoal_threshold = self.compute_goal_threshold()
        near_max_goal_thresholdoal_threshold =  round( (3/4) * max_goal_thresholdoal_threshold)
        average_total_goals = round( (1/2) * max_goal_thresholdoal_threshold)
        min_goalsoals_goal_threshold =  round( (1/4) * max_goal_thresholdoal_threshold)
        teams = self.get_league_teams()
        teams_data = self.compute_goals_scored_goals_conceded(teams,match_number)

        results = []
        for result in teams_data:
            goals_scored = int(result[1])
            goals_conceded = int(result[2])
            if (goals_conceded <= min_goalsoals_goal_threshold) and (goals_scored >= average_total_goals and goals_scored < near_max_goal_thresholdoal_threshold):
                results.append(result)

        return results
            
    def worst_teams(self,match_number):
        """
        worst teams.
        score less than minimum, concede more than average.
         
        """
        max_goal_thresholdoal_threshold = self.compute_goal_threshold()
        near_max_goal_thresholdoal_threshold =  round( (3/4) * max_goal_thresholdoal_threshold)
        average_total_goals = round( (1/2) * max_goal_thresholdoal_threshold)
        min_goalsoals_goal_threshold =  round( (1/4) * max_goal_thresholdoal_threshold)
        teams = self.get_league_teams()
        teams_data = self.compute_goals_scored_goals_conceded(teams,match_number)

        results = []
        for result in teams_data:
            goals_scored = int(result[1])
            goals_conceded = int(result[2])
            if (goals_scored <= min_goalsoals_goal_threshold) and (goals_conceded >= average_total_goals):
                results.append(result)

        return results

    def get_team_data(self,team_name,match_number):
        """Gets team data. total goals scored and conceded in 5 matches.
        """
        total_goals_scored_at_home = self.get_total_home_goals_scored(team_name,match_number)
        total_goals_scored_at_away = self.get_total_away_goals_scored(team_name,match_number)
        total_goals_scored = total_goals_scored_at_home + total_goals_scored_at_away
        
        total_goals_conceded_at_home = self.get_total_home_goals_conceded(team_name,match_number)
        total_goals_conceded_at_away = self.get_total_away_goals_conceded(team_name,match_number)
        total_goals_conceded = total_goals_conceded_at_home + total_goals_conceded_at_away
        
        return (team_name, total_goals_scored,total_goals_conceded)

        
    def rank_team(self,team):
        """
        Computes the rank of a team in the league.
        team: a tuple. ("Arsenal",10,6) where 5 = goals scored, 15 = goals conceded.
        rank 1: conceded less than min, scored more than max goals or near max goals.
        rank2: conceded less than min, scored above average goals.
        rank3: conceded btn min and average goals, scored above max goals.
        rank3: conceded btn min and avrage goals, scored above average.
        rank4: conceded above average, scored above average.
        rank5: conceded more than max, scored less than min goals.
        rank6: conceded more than max, scored above above average.
        rank7: conceded more than near_max_goal_thresholdgoals, scored above near or max goals.
        """
        goals_scored = team[0][1]
        goals_scored = int(goals_scored) # goals scored.
        #print("Total Goals Scored"+team[0][0],team[0][1])

        goals_conceded = team[0][2]
        goals_conceded = int(goals_conceded)# goals conceded
        #print("Goals conceded: ",goals_conceded)
        max_goal_threshold = self.compute_goal_threshold()
        #print("Goals: ",max_goal_threshold)
        near_max_goal_threshold= round((3/4) * max_goal_threshold)
        avg_goals = round((1/2) * max_goal_threshold)
        min_goals = round((1/4) * max_goal_threshold)
        #print("Type: ",min_goals)
        rank = 0
        comment = ""
        
        if (goals_conceded <= min_goals and goals_scored >= max_goal_threshold) or (goals_conceded <= min_goals and goals_scored >= near_max_goal_threshold):
            rank = 1
            comment = comment + "Best team: conceded less than min goals, scored above max goals."
            

        elif (goals_conceded <= min_goals and goals_scored >= avg_goals) or (goals_conceded <= min_goals and goals_scored >= near_max_goal_threshold):
            rank = 2
            comment = comment + "Second Best: Conceded less than min goals, scored above average goals."
        
        elif ((goals_conceded < avg_goals and goals_conceded > min_goals) and (goals_scored >= max_goal_threshold)) or ((goals_conceded < avg_goals and goals_conceded > min_goals) and goals_scored >= near_max_goal_threshold):
            rank = 3
            comment = comment + "Third best: conceded btn min and avg goals, scored above avg goals."
        elif (goals_conceded >= avg_goals or goals_conceded < near_max_goal_threshold ) and (goals_scored >= avg_goals and goals_scored < near_max_goal_threshold):
            rank = 4
            comment = comment + "Fourth: good for both teams to score."
        elif( goals_conceded >= near_max_goal_threshold and goals_scored < min_goals):
            rank = 5
            comment = comment + "Fifth: good for draw if both teams are like this. conceded alot scores less."
        elif (goals_conceded >= near_max_goal_threshold and goals_scored >= near_max_goal_threshold):
             rank = 6
             comment = comment + "conceded more than max goals, scored more than max goals."
        else:
            rank = 0
            comment = comment + "ungraded please RECHECK"
        return team, rank,comment
    
    def bet(self,rank1,rank2):
        """Computes the best bet.
        r1: The rank of the team. (tuple,rank:rank,comment)
        r2: rank of other team
        
        """
        bet = ""
        r1 = rank1[1] # rank
        r2 = rank2[1] #rank
        r1_name = rank1[0] # name of team
        r2_name = rank2[0] # name of team.
        #print("Betiing Method: Rank ",r1)
        #print("Betting Method: Tuple with Name: ",r1_name)

        if r1 == 1 and r2 >= 4:
            bet = bet + r1_name[0][0] + "To WIN!!"
        elif r2 == 1 and r2 >= 4: 
            bet = bet + r2_name[0][0] + "To WIN!!"
        elif r2 == 2 and r1 >= 4:
            bet = bet + r2_name[0][0] + "To Win!!"
        elif r1 == 2 and r2 >= 4:
            bet = bet + r1_name[0][0] + "To WIN!!"
        elif r1 == 3 and r2 >= 5:
             print("BET", r1_name[0][0])
             bet = bet + r1_name[0][0] + "To WIN!!"
        elif r2 == 3 and r1 >= 5:
            bet = bet + r2_name[0][0] + "To WIN!!"
        elif r1 == 3 and r2 >= 4:
            print("BBB",rank1[0])
            bet = bet + r1_name[0][0] + "Win or draw"
        elif r1 == 4 and r2 == 4:
            bet = bet + "Both teams to score!!"
        elif r1 == 5 and r2 == 5:
            bet = bet + "Draw: "
        elif r1 == 6 and r2 == 6:
            bet = bet + "Both teams to score." 
        elif r1 == 0 and r2 == 0:
            bet = bet + "Avoid bet!!"
        return bet    








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
          
           #home_team = league.compute_goals_scored_goals_conceded(teams,match_number)
           #away_team = league.compute_goals_scored_goals_conceded(teams,match_number)
           #print(home_team)
           #bet = bet4(league, homeTeam, awayTeam)
           #return (bet)
           home_team_data = league.get_team_data(homeTeam,match_number)
           #print("Team data: ",home_team_data)

           away_team_data = league.get_team_data(awayTeam,match_number)
           rank_home_team = league.rank_team(home_team_data)
           print("\n")
           print("Rank Home Team: ",rank_home_team )
           rank_tuple = rank_home_team[0]
           home_result = rank_tuple[0]
           print("Ranking Team: ",home_result[0])
           #print("Home Rank: ",home_result[1])
           print("Total Goals Scored: ",home_result[1])
           print("Total Goals Conceded: ",home_result[2])
           print("Rank: ",rank_home_team[2])
           print("\n")
           
           rank_away_team = league.rank_team(away_team_data)
           rank_away_tuple = rank_away_team[0]
           away_result = rank_away_tuple[0]

           print("Rank Away Team: ",rank_away_team)
           print("Ranking Team: ",away_result[0])
           print("Total Goals Scored: ",away_result[1])
           print("Total Goals Conceded: ",away_result[2])
           print("Rank: ",rank_away_team[2])

           bet = league.bet(rank_home_team,rank_away_team)

           return bet


def display_match_daySta(league,match_number):
    """Displays goals in ALL match days in the league.
       We need to make sense of this data.
       league: the league object. a dict.{matchday1:matchday1}
    """
    
    """
    match_days  = league.gget_match_days()
    print(match_days)
    for index in range(1,len(match_days) + 1):
        match_day_goals = league.get_match_day_goals(index)
        print(match_day_goals)
    """
    matches = league.get_ALL_match_day_Goals()
    total_goals = 0
    for m in matches:
        #total_goals = total_goals + m[0]m[-1]
        match_day = m[0]
        total_goals = total_goals + match_day[-1]
        #print(match_day[-1])
        #print(m[0])
    average = total_goals/len(matches)
    average = round(average,2)

    max_goal_thresholdoals_scored = league.compute_goal_threshold()
    near_max_goal_thresholdoals_scored = round( (3/4) * max_goal_thresholdoals_scored )
    average_goals_scored = round( (1/2) * max_goal_thresholdoals_scored )
    min_goalsoals_scored = round( (1/4) * max_goal_thresholdoals_scored )
    print("\nAverage goals per Match day: ",round(average))
    print("Maximum Goal Threshold in 5 Matches: ",league.compute_goal_threshold())
    print("Near Max goals scored:",near_max_goal_thresholdoals_scored)
    print("Average goals scored: ",average_goals_scored)
    print("Minimum goals scord: ",min_goalsoals_scored)
    
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
    print("\nStatistics of last Five Matches: ", team_name, sep="")
    print("Goals scored at home: ",total_goals_scored_at_home)
    print("Goals scored Away: ",total_goals_scored_at_away)
    print("Goals conceded at home: ",total_goals_conceded_at_home)
    print("Goals conceded Away: ",total_goals_conceded_at_away)
    print("\nSummary of  Five Matches:")
    for result in games_played:
        print(result)
    
    print("\nBet Tip:\n A team that has CONCEDED LESS GOALS in LAST 4 GAMES is STRONGER than a team that has CONCEDED MORE GOALS even though it has scored more goals. The LESS Goals a team CONCEDES the STRONGER it is.\nWARNING:\nDo not consider the goals scored. If two teams have CONCEDED the SAME NUMBER OF GOALS CONSIDER a DRAW or Dont bet on them.\nBet for the Stronger team to WIN, Numbers do not LIE.\nIgnore the home or Away. Just consider goals a team has conceded. Ignore exceptions..That is the pattern. Some big teams STAGE Losses, They do not want us to figure out the pattern. Especially 4 historical big 4 teams. e.g Arsenal,Chealsea, Sometimes they stage losses.\nIf odd is small for a win choose over 1.5 goals, its less risky")
    
 

def main():
    """Testing:
        England-League2 Test: No wrong prediction made.
        Spain Laliga Test: No wrong prediction. app avoids bogus bets.
        Germany: not good. gave two wrong answers.
        REPORT: good in league1 england.
    """
    #ENGLAND
    #filename="England_EPL_Season25_26.csv" # English Premier League.
    #filename="ENG_Championship.csv" # English Championship.
    #filename="ENG_National_League.csv" # England National League.
    #filename="ENG_League1.csv" # England League one.
    filename="ENG_League2.csv" # England League Two. 
    #filename="ENG_National_LeagueNorth.csv" # England National League NORTH.

    #FRANCE
    #filename="FRANCE_league1_Season25_26.csv" # FRENCH LEAGUE 1.
    #filename="FRANCE_division1.csv" # FRENCH DIVISION 1.

    #GERMANY
    #filename="Germany_Bundesliga_Season25_26.csv" # Germany Bundesliga.
    #filename="Germany_Division2.csv" #Germany Divion 2.

    #ITALY
    #filename="Italy_serieA_Season25_26.csv" #Italy Serie A.
    #filename="ITALY_SerieB.csv" Italy Serie B.

    #SPAIN f
    #filename = "Spanish_Laliga_Season_25_26.csv" #SPAIN LA-LIGA

    reader = csv.DictReader(open(filename, 'r') ) # load data from file.
    league = getData(filename,reader) # loads data to memory
    teams = league.get_league_teams()
    
    


    last_five_matches = 5
    match_number = len(league.get_ALL_match_day_Goals())
    match_number = match_number - last_five_matches
    # tracking matches from day10...modify to fit
    print("Bet Assistant!!!")
    display_match_daySta(league,match_number)
    
    myBet = menu(teams, league, match_number)
    print("\nCOMPUTER PREDICTIONS:From LAST 5 matches. ")
    print(myBet)
    print("If a team has conceded more than max goals and scored less than average. compare.")
    print("If one of the teams is ungraded and the other is gradede best. bet for best.")


if __name__ == "__main__":
    main()