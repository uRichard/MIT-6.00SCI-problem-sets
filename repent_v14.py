from datetime import date
import csv

"""Good Software should be: clear, scalable, efficient.
   This is good software. Allelua.
   Embrace OOP.
"""
class MatchDay:
    """
    Models a football match on a given day.
    This class will be used in modeling match days.
    Specifically in loading data from a CSV file.

    """
    def __init__(self,match_day,home_team, away_team, 
                home_team_score,away_team_score,
                half_time_home_goals=0, half_time_away_goals=0) -> None:
        """Constructs a matchday object.
        match_date: The match day of the Match, date. e.g 12/jan/2023
        home_team: The team playing at home, String.
        away_team: The visiting team, String.
        home_team_score: The score of the home team, integer.
        away_team_score: The score of the visiting team, integer
        """
        self.match_day = match_day
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
        return self.home_team +" "+str(self.home_team_score) +" Vs "+ " "+ str(self.away_team)+" "+str(self.away_team_score)  

class Team2:
    """Models a team with its performance. e.g goals scored, conceded, frequency of goals scored
     and goals conceded.
     """
    def __init__(self,name):
        self.name = name
        self.goals_scored = []
        self.goals_conceded = []
        self.freq_goals_scored = {}
        self.freq_goals_conceded = {}

class Team:
    """
    This class will be used to model a team.
    It will track the total goals scored and conced, say in
    last 5 or 3 matches.
    Note: Embrace OOP. 
    """
    def __init__(self, team_name, total_goals_scored,total_goals_conceded,num) -> None:
        """Creates a team object.
        team_name: The name of the team, String.
        total_goals_scored: scored goals in last 3 or 5 matches
        total_goals_conceded: conceded goals in last 3 or 5 matches.
        num: The number of last matches, Integer.e.g 5 or 3.
        """
        self.team_name = team_name
        self.total_goals_scored = total_goals_scored
        self.total_goals_conceded = total_goals_conceded
        self.num = num

    def __str__(self) -> str:
        """Returns string represention of the team object.
        return: string
        """
        return self.team_name+": "+"Total Goals Scored: "+str(self.total_goals_scored)+","+" Total Goals Conceded: "+str(self.total_goals_conceded)+" in last "+str(self.num)+" Matches."   

class League:
    """Models a single league, e.g La Liga""" 
    def __init__(self,reader) -> None:
        """Constructs a league object and loads data into the program.
        reader: object for reading csv files.
        databank: a dictionary that maps a matchday to a list of match objects.
        Example: {1:[Match,Match], 2:[Match,Match]}
        Note: Embrace OOP.
        """
        self.data_bank = {}
        self.getData(reader)

    def getData(self,reader):
        """
        loads data from file and adds to dictionary.
        filename: The name of the file. e.g filename = "EPL.csv"
        reader: The file reader for reading csv files.
        return: league object.
         csv variables: Div,Date,Time,HomeTeam,AwayTeam,FTHG,FTAG
        """
        dates = []
        counter = 0
        for row in reader:
            matchdate = row['Date'] 
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']
            home_team_score = row['FTHG']
            away_team_score = row['FTAG']
            #half_time_home_goals = row['halfTime_home_team_goals']
            #half_time_away_goals = row['halfTime_away_team_goals']

            #print(m_day,home_team_score, ":",away_team_score, away_team )
            #print("Away Team Score: ",away_team_score)
            
            #matchdate = "08/08/2025"
            matchdate = matchdate.split("/")
            day =   int(matchdate[0])
            month = int(matchdate[1])
            year = int(matchdate[2])
            match_date = date(year,month,day)
            
            #print(matchdate,home_team," " ,home_team_score, ":",away_team_score, away_team )
            
        
            home_team_score = int(home_team_score)
            away_team_score = int(away_team_score)
            #half_time_home_goals = int(half_time_home_goals)
            #half_time_away_goals = int(half_time_away_goals)
            
            if not (match_date in dates):
                counter = counter + 1
                dates.append(match_date)
            
            
            match_day = MatchDay(counter,home_team, away_team,
                                home_team_score, away_team_score,
                                )

            self.add_match_day(counter, match_day)
                 
    def add_match_day(self, index, match):
        """
        Adds a match object to the league object.
        match_date: The date of a match day.
        match: The match object.
        to achieve: {1/3/2025:[1,(manU,Arsenal,2,3),(...),(...)]}
        where (manU,Arsenal,2,3) is a match object.
        e.g{1:[Match,Match2,Match2),..],...}
          
        """ 
        #matches = []   
        if not index in self.data_bank:
            matches = []
            
            self.data_bank[index] = matches
            self.data_bank[index].append(match)


        else:
            self.data_bank[index].append(match)

    def get_matches_played(self, team_name):
        """
        Computes and returns all the matches a team has played.
        team_name: The name of the team, String.
        matches: dictionary. {1:[Match1,Match2],2:[Match3,..]}
        return: list of MatchDay objects. e.g [MatchDay, MatchDay,..]
        Note: Embrace OOP.
        """
        results = []
        
        for key in self.data_bank:
            for match in self.data_bank[key]:
                hometeam = match.home_team
                awayteam = match.away_team
                if team_name == hometeam or team_name ==  awayteam:
                    results.append(match)
        result = sorted(results, key = lambda match: match.match_day)            
        return result   
    
    def get_match_day(self, num):
        """Computes and returns matches played on the full match day.
        A full match day is one with 4 or more games
        num: the number of a match day. e.g Match day 3.
        To get the last match day find the maximum key.
        If that key has few games, subtract one and get
        another for indexing.
        """
        keys = self.data_bank
        max_key = max(keys) # max key is the last match.
        return self.data_bank[num]
    
    def get_index(self):
        """Computes and returns the index for last match day.
        This is useful if we wish to find the games in last match day.
        We do this by indexing in the data bank storage.
        
        """
        indexes = self.data_bank.keys()
        max_index = max(indexes)
        return max_index

    def get_last_games(self, team_name, num):
        """Computes and returns any last number of games the team has played.
        Use: suppose we wish to get the last two games. We use this method.
        team_name: The name of a team.
        num: The number of games you wish to return.
        return list of MatchDay objects.
        """
        last_played = self.get_matches_played(team_name)
        index = len(last_played) - num
        return last_played[index:]
     
    def get_first_games(self, team_name, num):
        """
        Computes and returns the first games.
        Say you wish to find the first 3 games, use this method.
        team_name: The name of a team, String.
        num: The number of the first matches, integer.
        return: list of objects.
        """
        first_played = self.get_matches_played(team_name)
        #index = num + 1#watch for index error.
        return first_played[0:num]

    def get_goals_conceded(self, team_name, num):
        """
        Computes and returns the total goals conceded by a team 
        in last 5 or 3 depending on the value of the variable num(number)
        For now whether the team is either playing home or away.
        tesm_name: The name of the team, String.

        """
        last_matches = self.get_last_games(team_name,num)
        total = 0
        for match in last_matches:
            #print(match)
            hometeam = match.home_team
            awayteam = match.away_team
            homescore = match.home_team_score
            awayscore = match.away_team_score
            if team_name == hometeam:
                total = total + awayscore
            elif team_name == awayteam:
                total = total + homescore

        return total
   
    def goals_conceded(self,team_name, num):
        """Computes and returns the list of goals conceded by a team.
         return:list e.g [1,2,3,4]
        """
        last_matches = self.get_last_games(team_name,num)
        total = []
        for match in last_matches:
            #print(match)
            hometeam = match.home_team
            awayteam = match.away_team
            homescore = match.home_team_score
            awayscore = match.away_team_score
            if team_name == hometeam:
                #total = total + awayscore
                total.append(awayscore)
            elif team_name == awayteam:
                #total = total + homescore
                total.append(homescore)
        return total
   
    def get_goals_scored(self, team_name, num):
        """Computes and returns the number of goals scored by a team
        in the last 5, 3 matches depending on the value of num(number).
        team_name: The name of the team, String.
        num: The number of last matches.
        Note: Embrace OOP.
        """
        last_matches = self.get_last_games(team_name,num)
        total = 0
        for match in last_matches:
            #print(match)
            hometeam = match.home_team
            awayteam = match.away_team
            homescore = match.home_team_score
            awayscore = match.away_team_score
            if team_name == hometeam:
                total = total + homescore
            elif team_name == awayteam:
                total = total + awayscore

        return total

    def goals_scored(self,team_name,num):
        """Computes and returns the list of goals scored.
        return: list e.g [1,2,3,4]
        """
        last_matches = self.get_last_games(team_name,num)
        total = []
        for match in last_matches:
            #print(match)
            hometeam = match.home_team
            awayteam = match.away_team
            homescore = match.home_team_score
            awayscore = match.away_team_score
            if team_name == hometeam:
                #total = total + homescore
                total.append(homescore)
            elif team_name == awayteam:
                #total = total + awayscore
                total.append(awayscore)
        return total
    
    def get_freq(self,goals):
        """Computes and returns the frequency of goals.
       return: dict, e.g {1:3,2:1} key is goal, value is frquency.
       """
        goals = goals[:] #create a copy.
        freq = {}
        for g in goals:
            if not g in freq:
                freq[g] = 1
            else:
                freq[g] += 1
        return freq

    def get_teams(self):
        """
        Computes and returns the all the teams in the league.
        return:list of teams of type String.
        """
        results = []
        for key in self.data_bank:
            for match in self.data_bank[key]:
                hometeam = match.home_team
                awayteam = match.away_team
                if not hometeam in results or not awayteam in results:
                    results.append(hometeam)
        teams = sorted(results)
        return teams       

    def get_team_data(self,team_name,num):
        """
        Computes and returns data about the team,
        where the data is the goals scored and goals conceded.
        team_name: The name of the team, String.
        num: The number of the last matches.
        Note: Embrace OOP.
        """
        total_goals_scored = self.get_goals_scored(team_name, num)
        total_goals_conceded = self.get_goals_conceded(team_name, num)
        team = Team(team_name, total_goals_scored, total_goals_conceded,num)
        return team

    def get_league_data(self,num):
        """
        Computes and returns the data of every team in the league.
        """
        results = []
        teams = self.get_teams()
        for team in teams:
            team_data = self.get_team_data(team,num)
            
            results.append(team_data)
        return results
    
    def get_average_goals(self):
        """Computes and returns the average goals in a match day.
           
        """
        index = self.get_index()

        last_matches = self.get_match_day(index)
        second_last = self.get_match_day(index - 1)
        third_last  = self.get_match_day(index - 2)
        matches = last_matches + second_last + third_last
        num = len(matches)
        total = 0
        for m in matches:
            hs = m.home_team_score
            aw = m.away_team_score
            total = total + hs + aw
        average_goals = round(total/num)
        return average_goals     

    def get_BTTS(self,team_name,num):
        """Computes and returns BTTS(Both teams to score.)
        team_name: The name of the team.
        team_data: Team(scored,conceded)
        num: The number of last matches.
        Consider the last game in last matchday,
        check if it has conceded min threshold.
        work backward and see if it can score half or more goals.
        Work forwards, has it scored min threshold,
        then work backward to see if it has conceded half goals.
        We return the team that has conceded those goals.
        Embrace OOP.
        """
        result = ""
        goal_threshold = self.get_average_goals()
        Max_goals = 3 * goal_threshold #for last three games.
        avg_goals = round((1/2) * Max_goals)
        #work backwards, see what it conceded in last match.
        team = self.get_team_data(self,team_name,1)
        goals_scored = team.total_goals_scored
        goals_conceded = team.total_goals_conceded

        #check if team conceded the min threshold in last match.
        if goals_conceded >= goal_threshold:
            team_data_ = self.get_team_data(self,team_name,3) #data for last three matches.
            goals_scored_ = team_data_.total_goals_scored
            if goals_scored_ >= avg_goals:
                result = result +"Both teams to score."

        elif goals_scored >= goal_threshold:
            team_data_2 = self.get_team_data(self,team,3)
            goals_conceded = team_data_2.total_goals_scored
            if goals_conceded >= avg_goals:
                result = result + "Both teams to score."

        return result
         
    def find_trend(self,team_name):
        """Returns data of two teams."""
        result = []
        num = [1,2,3,4,5,6,7,8,9,10,15,19] # 1 for last game, 2 for second last gameetc.
        for n in num:
            team_data = self.get_team_data(team_name,n)
            result.append(team_data)
        return result

def main():
    """Loads data from csv and tests the computations."""
    #ENGLAND
    #filename= "E0.csv" # English Premier League.
    #filename = "E1.csv" #English Championship
    #filename = "E2.csv" #English League 1
    #filename = "E3.csv" #"ENGLISH_LEAGUE2.csv" # English League2
    #filename = "EC.csv" # English National League.
    
    
    #FRANCE
    #filename="F1.csv" # FRENCH LEAGUE 1.
    #filename="F2.csv" # FRENCH DIVISION 1.


    #GERMANY
    #filename = "D1.csv"
    #filename = "D2.csv"

    #Switzerland
    #filename = "SWZ.csv"

    #ITALY
    #filename="I1.csv" #Italy Serie A.
    #filename="I2.csv" #Italy Serie B.


    #SPAIN f
    #filename = "SP1.csv" #LALIGA1
    filename = "laliga2_.csv" #SPAIN LA-LIGA 2
    

    #SCOTLAND
    #filename = "SC0.csv" #scotland premier league.
    #filename = "SC1.csv" #scotland division one.
    #filename = "SC2.csv" #scotland league2
    #filename = "SC3.csv" #scotland league2
    
    #NETHERLANDS
    #filename = "N1.csv"
    
    #BELGIUM
    #filename = "B1.csv"
    
    #GREECE
    #filename = "G1.csv"

    #Romania
    #filename = "ROU.csv"

    #AUSTRIA
    #filename = "AUT.csv" #AUSTRIA
    
    #DENMARK
    #filename = "DNK.csv"
    
    #sweden
    #filename = "SWE.csv"
    
    #Poland
    #filename = "POL.csv"

    #MEXICO
    #filename = "MEX.csv"
    

    #Turkey
    #filename = "T1.csv"
    
    #Portugal
    #filename ="P1.csv"

    #Argentina
    #filename = "ARG.csv"

    #Brazil
    #filename = "BRA.csv"

    #USA
    #filename = "USA.csv" #not latest.

    #Japan
    #filename = "JPN.csv"

    #China
    #filename = "CHN.csv"

    reader = csv.DictReader(open(filename, 'r') )
    league = League(reader)
    
    
    num_of_last_matches = 3                                                                    
    
    
    team_data = league.get_league_data(num_of_last_matches)
    print("League Data: ")
    for team in team_data:
        print("\n",team)
    
    print("\nGames on last Matchday:")
    gg = league.get_match_day(league.get_index() - 1)
    for g in gg:
        print(g)
       
    
    #testing goals scored,conceded, frquency etc
    """team = "Man City"
    num_of_last_matches = 7
    goals_scored = league.goals_scored(team,num_of_last_matches)
    freq_goals_scored = league.get_freq(goals_scored)
    goals_conceded = league.goals_conceded(team,num_of_last_matches)
    freq_goals_conceded = league.get_freq(goals_conceded)
    print("Goals Scored: ",goals_scored)
    print("Goals Scored Frequency: ",freq_goals_scored)
    print("\nGoals Conceded: ",goals_conceded)
    print("Frequency of Goals Conceded: ",freq_goals_conceded)
    print("\nABOUT: key: value\ne.g 1:2 Twice he has scored or conceded 1 goals.")
    """


    home_team_name = "Paris FC" #Add home team   
    last_matches = league.get_last_games(home_team_name, num_of_last_matches)
    print("\nLast "+str(num_of_last_matches)+" Games:",home_team_name)
    for m in last_matches:
        print("MatchDay: "+str(m.match_day),m)   
    
    away_team_name = "Le Havre" #Add away team
    last_matches = league.get_last_games(away_team_name, num_of_last_matches)
    print("\nLast "+str(num_of_last_matches)+" Games:",away_team_name)

    for m in last_matches:
        print("MatchDay: "+str(m.match_day),m)   
    
    trend_home_team = league.find_trend(home_team_name)
    print("\nTrend in last Matches: ")
    for t in trend_home_team:
        print(t)
    
    trend_away_team = league.find_trend(away_team_name)
    print("\n")
    for t in trend_away_team:
        print(t)

    avg = league.get_average_goals()
    print("\nAverage Goals in Last three match days: ",avg)
    
    #Frequency:
    print("\nSummary:",home_team_name)
    num_of_last_matches = 10#lets look at last 7 matches.
    
    goals_scored = league.goals_scored(home_team_name,num_of_last_matches)
    #goals_scored = goals_scored.re
    freq_goals_scored = league.get_freq(goals_scored)
    goals_conceded = league.goals_conceded(home_team_name,num_of_last_matches)
    freq_goals_conceded = league.get_freq(goals_conceded)
    print("Goals Scored: ",goals_scored)
    print("Goals Scored Frequency: ",freq_goals_scored)
    print("\nGoals Conceded: ",goals_conceded)
    print("Frequency of Goals Conceded: ",freq_goals_conceded)

    print("\nSummary:",away_team_name)
    goals_scored_away_ = league.goals_scored(away_team_name,num_of_last_matches)
    freq_goals_scored_away_ = league.get_freq( goals_scored_away_)
    goals_conceded_away_ = league.goals_conceded(away_team_name,num_of_last_matches)
    freq_goals_conceded_away_ = league.get_freq(goals_conceded_away_ )
    print("Goals Scored: ",goals_scored_away_ )
    print("Goals Scored Frequency: ",freq_goals_scored_away_)
    print("\nGoals Conceded: ",goals_conceded_away_)
    print("Frequency of Goals Conceded: ",freq_goals_conceded_away_)
    print("\nABOUT: key: value\ne.g 1:2 Twice he has scored or conceded 1 goals.\nGoals:[1,2,3,4], the last element is the first goal i.e most recent match, 4.")

    """
    print("Average means ANY team can score such GOALS in the league. Good for the assumptions we make instead of using 2.")
    print("Identify a team that converges and one that diverges from being a better team. our assumption 2 goals per game conceding none. Avoid 1\n\nBet by RULES, find games that the company wants you to win.") 
    print("\nHas a team conceded tice in a sinle match?")
    print("\nObservations:")
    print("\nNotice if a team has scored average or above average. A team that scores average or above average from last 2 to 5 games, will score.")
    """
    
    
    
    """
    matches = league.get_matches_played("Coventry")
    for match in matches:
        print("Matchday "+str(match.match_day)," ",match)
    
    last_matches = league.get_last_games("Coventry",5)
    print("Last 5 Games: ")
    for m in last_matches:
        print("MatchDay: "+str(m.match_day),m)

    first_matches = league.get_first_games("Coventry",3)
    print("\nFirst 3 Matches: ")
    for m in first_matches:
        print("MatchDay "+str(m.match_day),m)
    
    goals_conceded = league.get_goals_conceded("Coventry",5)
    print("\nTotal Goals Conceded in Last 3 Matches: ",goals_conceded)  
    goals_scored = league.get_goals_scored("Coventry",5)
    print("\nGoals Scored in last 3 matches: ",goals_scored)

    print("Team Data: ")
    team_data = league.get_team_data("Coventry",5)
    print(team_data)

    print("All teams in the league: ")
    teams = league.get_teams()
    print(teams)
    """ 
if __name__ == "__main__":
    main()
