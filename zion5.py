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
                home_team_score,away_team_score,bet_homewin,bet_draw,bet_awaywin):
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
        self.bet_homewin = bet_homewin
        self.bet_draw = bet_draw
        self.bet_awaywin = bet_awaywin
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
    
    def display(self,visible):
        """returns String representation of a MatchDay object."""
        result = ""
        if visible == True:
           result = result+self.home_team +" "+str(self.home_team_score) +" Vs "+ " "+ str(self.away_team)+" "+str(self.away_team_score)  
        else:
            result = result+self.home_team +" Vs "+self.away_team +"\n"+"1: "+str(self.bet_homewin)+" "+"x: "+str(self.bet_draw)+" "+"2: "+str(self.bet_awaywin)
        return result

    def __str__(self):
        """returns String representation of a MatchDay object."""
        return self.home_team +" "+str(self.home_team_score) +" Vs "+ " "+ str(self.away_team)+" "+str(self.away_team_score)  

class Team:
    """
    This class will be used to model a team.
    It will track the total goals scored and conced, say in
    last 5 or 3 matches.
    Note: Embrace OOP. 
    """
    def __init__(self, team_name, total_goals_scored,total_goals_conceded,num):
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

    def __str__(self):
        """Returns string represention of the team object.
        return: string
        """
        return self.team_name+": "+"Total Goals Scored: "+str(self.total_goals_scored)+","+" Total Goals Conceded: "+str(self.total_goals_conceded)+" in last "+str(self.num)+" Matches."   

class League:
    """Models a single league, e.g La Liga""" 
    def __init__(self,reader):
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
            odd_home_team_win = row['B365H']
            odd_draw = row['B365D']
            odd_away_team_win = row['B365A']
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
                                odd_home_team_win, odd_draw,odd_away_team_win)

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
    
    def get_team_data(self,team_name,match_day, num):
        """
        Computes and returns data about the team,
        where the data is the goals scored and goals conceded.
        team_name: The name of the team, String.
        num: The number of the last matches.
        Note: Embrace OOP.
        """
        total_goals_scored = self.get_goals_scored(team_name, match_day, num)
        total_goals_conceded = self.get_goals_conceded(team_name, match_day, num)
        team = Team(team_name, total_goals_scored, total_goals_conceded, num)
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
    
    def find_trend(self,team_name,match_day,num):
        """Returns data of two teams.
        match_day: The match day number.
        num: The number of last previous matches.
        """
        result = []
        """num = [1,2,3,5,6,7,8,9,10,15,20] # 1 for last game, 2 for second last gameetc.
        for n in num:
            team_data = self.get_team_data(team_name,match_day, n)
            result.append(team_data)   
        """
        last_matches = self.find_matches_played(team_name, match_day, num)
        for i in range(1,len(last_matches) + 1):
            team_data = self.get_team_data(team_name,match_day, i)
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
        passed = 0
        failed = 0
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
                #print(p,players_hand[p].display(False))
            #-------------
            match = players_hand[start_key]
            match_day_num = match.match_day
            #add logic for previous match statistics.
            #to be implemented
            #------------------------------
            #Here..
            home_team_name = match.home_team
            away_team_name = match.away_team
            """
            previous_matches_home_team = self.find_matches_played(home_team_name,match_day_num)
            print("\nAll Previous Matches: ",home_team_name)
            for p in previous_matches_home_team:
                print(p)
            """
            previous_matches_home_team = self.get_last_matches_played(home_team_name,match_day_num)
            print("\nLast 4 Matches: ",home_team_name)
            for p in previous_matches_home_team:
                print(p.match_day,p)

            #print("Goals Conceded: ",self.get_goals_conceded(home_team,match_day_num))
            #print("\nGoals scored in last games:",self.get_goals_scored(home_team,match_day_num))
            """
            previous_matches_away_team = self.find_matches_played(away_team_name,match_day_num)
            print("\nAll Previous Matches: ",away_team_name)
            for p in previous_matches_away_team:
                print(p)
            """
            previous_matches_away_team = self.get_last_matches_played(away_team_name,match_day_num)
            print("\nLast 4 Matches: ",away_team_name)
            for p in previous_matches_away_team:
                print(p.match_day,p)


            #trend_home_team = self.find_trend(home_team_name, match_day_num)
            trend_home_team = self.find_trend(home_team_name, match_day_num,15)
            print("\nTrend in last Matches: ",home_team_name)
            for t in trend_home_team:
                print(t)
    
            #trend_away_team = self.find_trend(away_team_name, match_day_num)
            trend_away_team = self.find_trend(away_team_name, match_day_num,15)
            print("\n")
            print("\nTrend in last Matches: ",away_team_name)
            for t in trend_away_team:
                print(t)
            
            avg = self.get_average_goals(match_day_num)
            print("\nAverage Goals in Last three match days: ",avg)
            print("Matchday Number: ",match_day_num)
            print("Passed: ",passed)
            print("Failed: ",failed)
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
                        passed += 1
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
                        failed += 1
                        print("Try Again.")
                        tt = input("Try Again. Enter t ")
                        ##do nothing

                elif cmd == 2:
                    result = self.bet(match,cmd)
                    print("RESULT: ",result)
                    if result == "WIN":
                        passed += 1
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
                        failed += 1
                        print("Please Try Again.")
                        tt = input("Try Again. Enter t ")

            elif not cmd.isnumeric():
                if cmd == "x":            
                    result = self.bet(match,cmd)
                    print("RESULT: ",result)
                    if result == "WIN":
                        passed += 1
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
                        failed += 1
                        print("Please Try Again.")
                        tt = input("Try Again. Enter t")
                elif cmd == "n":
                     result = self.bet(match,cmd)
                     print("RESULT: ",result)
                     if result == "WIN":
                        passed += 1
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
                        failed += 1
                        print("Please Try Again.")
                        tt = input("Try Again. Enter t: ")

                elif cmd == "y":
                    result = self.bet(match,cmd)
                    print("RESULT: ",result)
                    if result == "WIN":
                        passed += 1
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
                        failed += 1
                        print("Please Try Again.")
                        tt = input("Try Again. Enter t: ")
                elif cmd == "exit":
                    sys.exit()
    
    def find_matches_played(self,team_name,match_day,num):
        """Computes and returns the matches played by a given team
        before a given match day.
        team_name: The name of the team, String.
        match_day: The match day, Integer.
        num: number of previous games.
    
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
        
        result = sorted(results, key = lambda match: match.match_day)            
        previous_matches = result[-1:0:-1]
        previous_matches = previous_matches[0:num]
        return previous_matches

    def get_goals_conceded(self, team_name, match_day, num):
        """
        Computes and returns the total goals conceded by a team 
        in last 5 or 3 depending on the value of the variable num(number)
        For now whether the team is either playing home or away.
        tesm_name: The name of the team, String.

        """
        last_matches = self.find_matches_played(team_name, match_day, num)
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

    def get_goals_scored(self, team_name,match_day,num):
        """Computes and returns the number of goals scored by a team
        in the last 5, 3 matches depending on the value of num(number).
        team_name: The name of the team, String.
        num: The number of last matches
        match_day:The match day. 
        Note: Embrace OOP.
        """
        
        last_matches = self.find_matches_played(team_name,match_day,num)
       
        total = 0
        for match in last_matches:
            #print(match)
            hometeam = match.home_team
            awayteam = match.away_team
            homescore = match.home_team_score
            #print("Debugging:",hometeam, homescore)
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
        #second_last = self.data_bank[match_day_num - 2] #self.get_match_day(match_day_num - 2)
        #third_last  = self.data_bank[match_day_num - 2] #self.get_match_day(match_day_num - 3)
        matches = last_matches# + second_last + third_last
        num = len(matches)
        total = 0
        for m in matches:
            hs = m.home_team_score
            aw = m.away_team_score
            total = total + hs + aw
        average_goals = round(total/num)
        return average_goals     
    
    def get_last_matches_played(self,team_name,match_day):
        """Computes and returns last 4 matches played by a given team.
        """
        matches = self.find_matches_played(team_name,match_day,4)
        #matches = matches[-1:0:-1]
        #matches = matches [0:4]
        return matches

def main():
    """Loads data from csv and tests the computations."""
    #ENGLAND
    #filename = "E0.csv" # English Premier League.
    #filename = "E0_2021_22.csv" #English Premier League 2021/22
   
    #filename = "E1.csv" #English Championship
    #filename = "E1_2008_2009.csv" #championship old
    #filename = "E1_2010_2011.csv"
    #filename = "E2.csv" #English League 1 #start at MATCHDAY 14
    #filename ="E2_2023_2024.csv" #start at MATCHDAY 16
    #filename = "E3.csv" #"ENGLISH_LEAGUE2.csv" # English League2
    #filename = "E3_2023_24.csv"
    
    #filename = "EC.csv" # English National League.
    
     #FRANCE
    #filename="F1.csv" # FRENCH LEAGUE 1.
    #filename="F2.csv" # FRENCH DIVISION 1.
    #filename = "F2_2021_22.csv"


    #GERMANY
    #filename = "D1.csv"
    #filename = "D1_2021_2022.csv" # season 2021/22
    #filename = "D2.csv"
    #filename = "D2_2021_22.csv" # season2021/22
    #filename = "D1_2021_2022.csv"
    #Switzerland
    #filename = "SWZ.csv"

    #ITALY
    #filename="I1.csv" #Italy Serie A.
    #filename="I2.csv" #Italy Serie B.
    #filename = "I2_20_21.csv" # start at MATCHDAY 40


    #SPAIN f
    #filename = "SP1.csv" #LALIGA1
    #filename = "SP2.csv" #SPAIN LA-LIGA 2
    

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
    #filename = "AUSTRIA_BUNDESLIGA.csv" #AUSTRIA
    
    #DENMARK
    #filename = "DNK.csv"
    
    #SWITZERLAND from 2012
    #filename = "SWZ.csv"
    
    #FINLAND from 2012
    #filename = "FIN.csv"
    
    #IRELAND from 2012
    #filename = "IRL.csv"
    
    #POLAND from 2012
    #filename = "POL.csv"
    
    #ROMANIA from 2012 start at matcday 119
    #filename = "ROU.csv"

    #MEXICO from 2012
    #filename = "MEX.csv"
    

    #Turkey
    #filename = "T1.csv"
    
    #Portugal
    #filename ="P1.csv"
    
    #SCOTLAND
    #filename = "SCO.csv"
    
    #USA from 2012
    #filename = "USA.csv"
    
    #ARGENTINA from 2012
    #filename ="ARG.csv"
    
    #BRAZIL from 2012
    #filename = "BRA.csv"
    
    
    #RUSSIA from 2012
    #filename = "RUS.csv"
    
    #SWEDEN from 2012
    #filename = "SWE.csv"
    
    #CHINA from 2012
    #filename = "CHN.csv"
    
     #Japan
    filename = "JPN.csv"

    reader = csv.DictReader(open(filename, 'r') )
    league = League(reader) #loading data to memory.
    
    """
    matches = league.find_matches_played("DC United",10,2) #matchday 10
    for m in matches:
        print(m.match_day,m)
        
    goals_scored = league.get_goals_scored("DC United",10,2) #last 3 games
    print("Goals:",goals_scored)
    goals_conceded = league.get_goals_conceded("DC United",10,2)
    print("Goals Conceded: ",goals_conceded)
    trend = league.find_trend("DC United",10,3) # 10 matchday 10, 3=last 3 matches.
    for t in trend:
        print(t)
    """

    
    #testing the hand method.
    #lets get a hand at some matchday. e.g 10,12,13
    #It works correctly.
    #let default hand be at match day 10.
    print("Hand:In Main method.")
    match_day_hand = 9
    hand = league.deal_hand(match_day_hand) # matches at match day 4. we shall start at last match day.
    for key in hand:
        print(key,hand[key])

    

    
    #Testing playhand(hand) method.
    # this interacts with a player so he can predict the outcome of a match.   
    league.play_hand(hand)
    
if __name__ == "__main__":
    main()
