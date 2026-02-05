from datetime import date
import csv,sys

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
                home_team_score,away_team_score ):
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
        #self.half_time_home_goals = half_time_home_goals
        #self.half_time_away_goals = half_time_away_goals

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
    
    def display(self,visible) -> str:
        """returns String representation of a MatchDay object."""
        result = ""
        if visible == True:
           result = result+self.home_team +" "+str(self.home_team_score) +" Vs "+ " "+ str(self.away_team)+" "+str(self.away_team_score)  
        else:
            result = result+self.home_team +" Vs "+self.away_team
        return result

    def __str__(self) -> str:
        """returns String representation of a MatchDay object."""
        return self.home_team +" "+str(self.home_team_score) +" Vs "+ " "+ str(self.away_team)+" "+str(self.away_team_score)  

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
        self.getData(reader) #loads data to memory or data bank.

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
    
    def deal_hand(self,key):
        """Computes and returns the matches in a specific matchday.
        These are the matches we wish to predict. This is a hand.
        The default hand will be at match day 10.
        key:The key to index in the databank, Integer.
        return: a dict. e.g {1:Match1, 2:Match} for some matchday.
        """

        matches = self.data_bank[key]
        results = {}
        index = 0
        for m in matches:
            index = index + 1
            results[index] = m
        return results
    
    def bet(self,match,decision):
        """Checks if the bet is right or wrong.
        """
        result = ''
        if decision == 1:
            if match.home_team_score > match.away_team_score:
                result = result + "WIN"
            else:
                result = result+"FAILED"
        elif decision == 2:
            if match.home_team_score < match.away_team_score:
                result = result + "WIN"
            else:
                result = result+ "FAILED"
        elif decision == "X" or decision == "x":
            if match.home_team_score == match.away_team_score:
                result = result +"WIN"
            else:
                result = result + "FAILED"
        elif decision == "y" or decision == "Y":
            if match.home_team_score > 0 and match.away_team_score > 0:
                result = result + "WIN"
            else:
                result = result + "FAILED" 
        elif decision == "n" or decision == "N":
            if match.home_team_score == 0 and match.away_team_score == 0:
                result = result + "WIN"
            else:
                result = result + "FAILED"    


        return result 
    
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
    
    def find_trend(self,team_name,num):
        """Returns data of two teams."""
        result = []
        #num = [1,2,3,4,5,6,7,8,9,10,15,19] # 1 for last game, 2 for second last gameetc.
        for n in range(1,num):
            team_data = self.get_team_data(team_name,n)
            result.append(team_data)
        return result

    def play_hand(self,hand):
        """This method  allows a player to play a given as hand as follows.
        A hand is a list of matches we wish the player to predict.
        hand: A dictionary. e.g {1: Match,2:Match,3:Match}
        1. Display the hand, one match at a time.
        2. The user inputs his prediction,
        e.g 1 for home team win or 2 for away team win or x for draw or y for BTTS.
        3. An invalid prediction is rejected and user is asked to try again.
        4. When a valid prediction is entered user is given a congratulation message.
        5. After a valid prediction, user is asked to go to next match in the hand.
        6.A hand is finished when user has gone through all the matches in the hand.
        """
        players_hand = hand.copy()
        keys = players_hand.keys()
        min_key = min(keys)
        counter = len(players_hand)
        start_key = min_key # every hand has some minimum key.
        while counter != 0:
            
            #----for testing: lets see the hand. remove later
            print("HAND: In playhand method!")
            for p in players_hand:
                print(p,players_hand[p])
            #-------------
            match = players_hand[start_key]
            match_day_num = match.match_day
            #add logic for previous match statistics.
            #to be implemented
            #------------------------------
            #Here..
            home_team_name = match.home_team
            away_team_name = match.away_team

            previous_matches_home_team = self.find_matches_played(home_team_name,match_day_num)
            print("\nAll Previous Matches: ",home_team_name)
            for p in previous_matches_home_team:
                print(p)
            #print("Goals Conceded: ",self.get_goals_conceded(home_team,match_day_num))
            #print("\nGoals scored in last games:",self.get_goals_scored(home_team,match_day_num))
            
            previous_matches_away_team = self.find_matches_played(away_team_name,match_day_num)
            print("\nAll Previous Matches: ",away_team_name)
            for p in previous_matches_away_team:
                print(p)

            trend_home_team = self.find_trend(home_team_name,match_day_num)
            print("\nTrend in last Matches: ")
            for t in trend_home_team:
                print(t)
    
            trend_away_team = self.find_trend(away_team_name,match_day_num)
            print("\n")
            for t in trend_away_team:
                print(t)
            
            avg = self.get_average_goals(match_day_num)
            print("\nAverage Goals in Last three match days: ",avg)
            
            #--------------------------------
            #display the hand to the user.
            print("\nPredict the Outcome:")
            print("\nBET: 1 Home WIN, 2 Away WIN, x Draw, y YES or n No for BTTS.")
            print("\n",match.display(False))
            cmd = input("Enter Prediction: ")
            if cmd.isnumeric():
                cmd = int(cmd)
                if cmd == 1:
                    result = self.bet(match,cmd)
                    print("RESULT: ",result)
                    if result == "WIN":
                        print(match.display(True))
                        print("Congratulations!!! You WIN.")
                        del players_hand[start_key] #remove it
                        enter = input("Enter q: for next Match. ")
                        if enter == "q":
                            if len(players_hand) > 0:
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                            elif len(players_hand) == 0:
                                #compute new hand.
                                match_day_num += 1
                                players_hand = self.deal_hand(match_day_num)
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                        
                        
                    else:
                        print("Try Again.")
                        tt = input("Try Again. Enter t ")
                        ##do nothing

                elif cmd == 2:
                    result = self.bet(match,cmd)
                    print("RESULT: ",result)
                    if result == "WIN":
                        print(match.display(True))
                        print("Congratulations!!! You WIN.")
                        del players_hand[start_key] #remove it
                        enter = input("Enter q: for next Match. ")
                        if enter == "q":
                            if len(players_hand) > 0:
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                            elif len(players_hand) == 0:
                                #compute new hand.
                                match_day_num += 1
                                players_hand = self.deal_hand(match_day_num)
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                        
                        
                    else:
                        print("Please Try Again.")
                        tt = input("Try Again. Enter t ")

            elif not cmd.isnumeric():
                if cmd == "x":            
                    result = self.bet(match,cmd)
                    print("RESULT: ",result)
                    if result == "WIN":
                        print(match.display(True))
                        print("Congratulations!!! You WIN.")
                        del players_hand[start_key] #remove it
                        enter = input("Enter q: for next Match ")
                        if enter == "q":
                            if len(players_hand) > 0:
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                            elif len(players_hand) == 0:
                                #compute new hand.
                                match_day_num += 1
                                players_hand = self.deal_hand(match_day_num)
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                        
                    else:
                        print("Please Try Again.")
                        tt = input("Try Again. Enter t")
                elif cmd == "n":
                     result = self.bet(match,cmd)
                     print("RESULT: ",result)
                     if result == "WIN":
                        print(match.display(True))
                        print("Congratulations!!! You WIN.")
                        del players_hand[start_key] #remove it
                        enter = input("Enter q: for next Match: ")
                        if enter == "q":
                            if len(players_hand) > 0:
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                            elif len(players_hand) == 0:
                                #compute new hand.
                                match_day_num += 1
                                players_hand = self.deal_hand(match_day_num)
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                        
                     else:
                        print("Please Try Again.")
                        tt = input("Try Again. Enter t: ")

                elif cmd == "y":
                    result = self.bet(match,cmd)
                    print("RESULT: ",result)
                    if result == "WIN":
                        print(match.display(True))
                        print("Congratulations!!! You WIN.")
                        del players_hand[start_key] #remove it
                        enter = input("Enter q: for next Match.")
                        if enter == "q":
                            if len(players_hand) > 0:
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key
                            elif len(players_hand) == 0:
                                #compute new hand.
                                match_day_num += 1
                                players_hand = self.deal_hand(match_day_num)
                                keys = players_hand.keys()
                                min_key = min(keys)
                                start_key = min_key

                    else:
                        print("Please Try Again.")
                        tt = input("Try Again. Enter t: ")
                elif cmd == "exit":
                    sys.exit()
    
    def find_matches_played(self,team_name,match_day):
        """Computes and returns the matches played by a given team
        before a given match day.
        team_name: The name of the team, String.
        match_day: The match day, Integer.
    
        """
        results = []
        match_day -= 1
        while match_day != 0:
            matches = self.data_bank[match_day]
            for match in matches:
                hometeam = match.home_team
                awayteam = match.away_team
                if team_name == hometeam or team_name ==  awayteam:
                    results.append(match)
            match_day -= 1
        return results    

    def get_goals_conceded(self, team_name, num):
        """
        Computes and returns the total goals conceded by a team 
        in last 5 or 3 depending on the value of the variable num(number)
        For now whether the team is either playing home or away.
        tesm_name: The name of the team, String.

        """
        last_matches = self.find_matches_played(team_name,num)
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

    def get_goals_scored(self, team_name, num):
        """Computes and returns the number of goals scored by a team
        in the last 5, 3 matches depending on the value of num(number).
        team_name: The name of the team, String.
        num: The number of last matches
        Note: Embrace OOP.
        """
        last_matches = self.find_matches_played(team_name,num)
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
    
    def get_average_goals(self,match_day_num):
        """Computes and returns the average goals in a match day.
           
        """
    
        last_matches = self.data_bank[match_day_num - 2] #self.get_match_day(match_day_num - 1)
        second_last = self.data_bank[match_day_num - 2] #self.get_match_day(match_day_num - 2)
        third_last  = self.data_bank[match_day_num - 2] #self.get_match_day(match_day_num - 3)
        matches = last_matches + second_last + third_last
        num = len(matches)
        total = 0
        for m in matches:
            hs = m.home_team_score
            aw = m.away_team_score
            total = total + hs + aw
        average_goals = round(total/num)
        return average_goals     

  
def main():
    """Loads data from csv and tests the computations."""
    #ENGLAND
    #filename = "E0.csv" # English Premier League.
    
    #SCOTLAND
    #filename = "SCO.csv"
    
    #USA
    filename = "USA.csv"

    reader = csv.DictReader(open(filename, 'r') )
    league = League(reader) #loading data to memory.

    #testing the hand method.
    #lets get a hand at some matchday. e.g 10,12,13
    #It works correctly.
    #let default hand be at match day 10.
    print("Hand:In Main method.")
    match_day_hand = 10 #starting at match dayu 40
    hand = league.deal_hand(match_day_hand) # matches at match day 4. we shall start at last match day.
    for key in hand:
        print(key,hand[key])

    

    
    #Testing playhand(hand) method.
    # this interacts with a player so he can predict the outcome of a match.   
    league.play_hand(hand)

if __name__ == "__main__":
    main()
