import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk

# Load the Data and Drop unneccessary columns 
defense = pd.read_csv("NFL Team Defense Statistics.csv")
defense.drop(["Gms", "Pts/G", "RYds/G", "PYds/G", "Yds/G"],  axis=1, inplace=True)
offense = pd.read_csv ("NFL Team Offense Statistics.csv")
offense.drop(["Pts/G", "RYds/G", "PYds/G", "Yds/G"],  axis=1, inplace=True)
teamwins = pd.read_csv ("NFLteams.csv")
teamwins.drop(["conf", "division", "div_rank", "sov", "sos"],  axis=1, inplace=True)

# Cleans up the data so that the teamwins dataframe has full team names instead of abbreviations
df1 = teamwins['team']
df1 = df1.sort_values(ascending=True)
df1 = df1.drop_duplicates()
df2 = defense ['Team']
df2 = df2.sort_values(ascending=True)
df2 = df2.sort_values(ascending=True)
df2 = df2.drop_duplicates()
convert_abbreviation_to_name = dict( zip( df1, df2) )
teamwins.replace( convert_abbreviation_to_name, inplace=True )

# Replace team names of team that changed names the span of the data to their current team name.
offense['Team'] = offense['Team'].replace(['San Diego Chargers'],'Los Angeles Chargers')
offense['Team'] = offense['Team'].replace(['Oakland Raiders'],'Las Vegas Raiders')
offense['Team'] = offense['Team'].replace(['St. Louis Rams'],'Los Angeles Rams')
defense['Team'] = defense['Team'].replace(['San Diego Chargers'],'Los Angeles Chargers')
defense['Team'] = defense['Team'].replace(['Oakland Raiders'],'Las Vegas Raiders')
defense['Team'] = defense['Team'].replace(['St. Louis Rams'],'Los Angeles Rams')
teamwins['team'] = teamwins['team'].replace(['San Diego Chargers'],'Los Angeles Chargers')
teamwins['team'] = teamwins['team'].replace(['Oakland Raiders'],'Las Vegas Raiders')
teamwins['team'] = teamwins['team'].replace(['St. Louis Rams'],'Los Angeles Rams')

# Merges offense with teamwin using the columns of team and season that does not included any missing data. 
offenseWins = pd.merge(offense, teamwins,
    left_on=['Team','season '],
    right_on=['team','season'], how='inner' )
# Drop repeating columns 
offenseWins.drop(["season", "team"],  axis=1, inplace=True)

# Merges defense with teamwin using the columns of team and season that does not included any missing data. 
DefenseWins = pd.merge(defense, teamwins,
    left_on=['Team','season'],
    right_on=['team','season'], how='inner' )
#Drop repeating columns 
DefenseWins.drop("team",  axis=1, inplace=True)

# Drop duplicates values of team so there is only 32 NFL teams 
teams = offenseWins.Team.drop_duplicates()

# Drop duplicates values of season so there is an unique list of season from 2010-2020
season = offenseWins["season "].drop_duplicates()

# Replace nan in playoff column when team fail to make the playoffs in offenseWins and DefenseWins.
offenseWins['playoff'] = offenseWins['playoff'].fillna('Did not make the playoffs')
DefenseWins['playoff'] = DefenseWins['playoff'].fillna('Did not make the playoffs')

# This function loops through offenseWins to collect data for the team that was selected. 
def info(data, selected):
    selectedInfo = []
    RushData = []
    PassData =[]
    WinData = []
    SeasonData = []
    RankingData = []
    for index,row in data.iterrows():
            if row["Team"]==selected:
                selectedInfo.append(row)
                RushData.append(row['RushYds'])
                PassData.append(row['PassYds'])
                WinData.append(row['wins'])
                RankingData.append(row['Ranking'])
                SeasonData.append(row['season '])
    return selectedInfo,RushData, PassData, WinData, SeasonData

# This function create a barchart that shows total rushing yards each from each season for the team that was selected. 
def Rushingchart(RushData, SeasonData, selected):
    plt.bar(SeasonData, RushData, alpha=0.5)
    plt.ylabel("Total Rushing Yards")
    plt.xlabel("Season ")
    plt.title(f"{selected}'s Total Rushing Yards From 2010-2020 Season")
    plt.tight_layout()
    return plt

# This function create a barchart that shows total passing yards each from each season for the team that was selected. 
def PassingChart(SeasonData,PassData, selected):
    plt.bar(SeasonData, PassData, alpha=0.5)
    plt.ylabel("Total Passing Yards")
    plt.xlabel("Season ")
    plt.title(f"{selected}'s Total Passing Yards From 2010-2020 Season")
    plt.tight_layout()
    return plt

# This function create a line graph that shows the games the team has won for each season.  
def WinsChart(SeasonData, WinData, selected):
    fig = plt.figure()
    plt.plot(SeasonData, WinData)
    plt.xlabel('Seasons')
    plt.ylabel('Total Games Won per Season')
    plt.title(f"{selected}'s Total Won Games From 2010-2020 Season")
    return fig

# This function loops through offenseWins to collects and writes the data for the team and season that was selected. 
def infobyYear(data,selected, selectedseason):
    selectedSeasonInfo = []
    for index, row in data.iterrows():
        if row["Team"]==selected:
            if row['season '] == selectedseason:
                selectedSeasonInfo.append(row)
                r = row['RushYds']
                PassingYds = row['PassYds']
                Wins = row['wins']
                playoff = row['playoff']
                games = row['Gms']
    c =st.container()
    c.write(f'Team Name: {selected}')
    c.write(f'Season: {selectedseason}')
    c.write(f'Total Rushing Yards: {r}')
    c.write(f'Total Passing Yards: {PassingYds}')
    c.write(f'Total Wins for the Season: {Wins}')
    c.write(f'Outcome of Season: {playoff}')
    return r, PassingYds

# This function creates a piechart that displays the team's percentages of rushing and passing yards for the season selected. 
def rushingvsPassingchart(r,PassingYds):
    labels = 'Rushing Yards', "Passing Yards"
    sizes = [r, PassingYds]
    explode = (0, 0.1) 
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')
    return plt

# This function display the desired charts of the overall team data from checking the options of charts. 
def chart(selected):
    useRushingchart = st.checkbox("Total Rushing Yards Chart", False)
    usePassingChart = st.checkbox("Total Pasing Yards Chart", False)
    useWinsChart = st.checkbox("Win Graph", False)
    if useRushingchart and usePassingChart and useWinsChart:
        st.pyplot(Rushingchart(RushData, SeasonData, selected))
        st.pyplot(PassingChart(SeasonData,PassData, selected))
        st.pyplot(WinsChart(SeasonData, WinData, selected))
    elif useRushingchart and usePassingChart:
        st.pyplot(Rushingchart(RushData, SeasonData, selected))
        st.pyplot(PassingChart(SeasonData,PassData, selected))
    elif useRushingchart and useWinsChart:
        st.pyplot(Rushingchart(RushData, SeasonData, selected))
        st.pyplot(WinsChart(SeasonData, WinData, selected))
    elif useRushingchart:
        st.pyplot(Rushingchart(RushData, SeasonData, selected))
    elif usePassingChart and useWinsChart:
        st.pyplot(PassingChart(SeasonData,PassData, selected))
        st.pyplot(WinsChart(SeasonData, WinData, selected))
    elif usePassingChart:
        st.pyplot(PassingChart(SeasonData,PassData, selected))
    elif useWinsChart:
        st.pyplot(WinsChart(SeasonData, WinData, selected))
    else:
        " "
    return

# This function loop through the offenseWins data to collects and writes the selected team's history of making the playoffs.  
def playoffsinfo(data, selected):
    playoffteaminfo = []
    for index, row in data.iterrows():
        if row["Team"]== selected:
            if row['playoff'] != "Did not make the playoffs":
                playoffteaminfo.append(row)
                playoff = row['playoff']
                season = row["season "]
                st.write(f'Season: {season} - {playoff}')
    return

# This function loop through the offenseWins data to collects and writes the selected team's previous SuperBowl wins. 
def superbowlinfo(data, selected):
    for index, row in data.iterrows():
        if row["Team"]== selected:
            if row['playoff'] == "WonSB":
                season = row["season "]
                st.subheader(f'Season: {season} ')
    return

# This function create a button for users to click to see the selected team's history of making the playoffs and outcomes.
def playoffbuttons():
    playoffs = st.button("Playoff Trips", False)
    if playoffs:
        playoffsinfo(data, selected)
    else: 
        " "
    return
# This create a button for users to click to see the selected team's previous SuperBowl wins and nothing will appear if the team has not won a SuperBowl in the past 11 seasons. 
def Superbowlbutton():
    wonSuperbowls = st.button("SuperBowls Wins", False)
    if wonSuperbowls:
        superbowlinfo(data, selected)
    else:
        " "
    return

# This function loops through the offenseWins data to collect and write the desired season's top ten ranking offensives. 
def OFcomparison10byseason (data, selectedseason):
    st.subheader(f'For the {selectedseason} Season, the Top 10 Offense:')
    for index, row in data.iterrows():
        if row["Ranking"] <= 10:
            if row['season '] == selectedseason:
                t = row['Team']
                rank = row['Ranking']
                playoff = row['playoff']
                st.write(f'Team: {t}, Offense Ranking: {rank}, Playoff Result: {playoff}')
    return

# This function loops through the DefenseWins data to collect and write the desired season's top ten ranking defensives. 
def DEcomparison10byseason(df5, selectedseason):
    st.subheader(f'For the {selectedseason} Season, the Top 10 Defense')
    for index, row in df5.iterrows():
        if row["Ranking"] <= 10:
            if row['season'] == selectedseason:
                t = row['Team']
                rank = row['Ranking']
                playoff = row['playoff']
                st.write(f'Team: {t}, Defense Ranking: {rank}, Playoff Result: {playoff}')
    return

# This function loops through both offenseWins and DefenseWins to collect and write the superbowl champion for the selected season with the team's offesive and defensive rank that season. 
def superbowlchampbyseason(data,df5,selectedseason):
    for index, row in data.iterrows():
            if row["season "]== selectedseason:
                if row['playoff'] == "WonSB":
                    team = row["Team"]
                    Orank = row['Ranking']
    for index, row in df5.iterrows():
        if row["season"]== selectedseason:
                if row['playoff'] == "WonSB":
                    drank = row['Ranking']
    st.subheader(f'{team}')
    st.write(f'Offensive Rank: {Orank}')
    st.write(f'Defensive Rank: {drank}')
    return 

# Main loop

# Loads the data 
data = offenseWins 
df5 = DefenseWins

# Title and author  of the app 
st.header('Inside  Recent Trends in the NFL')
st.write("By Emily Blatt")

## Team Data Section 
# creates a drop down box for users to select which team they would like to examine.  
selected = st.selectbox('Select a NFL Teams', teams)

#Calls the info function and creates variables that contain data for selected team. 
selectedInfo,RushData, PassData, WinData, SeasonData = info(data, selected)

# Call the chart funtction to display the team's charts from click checkboxes.  
chart(selected)

# Calls the playoffbuttons function that display a button for users to press to see team's playoff history. 
playoffbuttons()

# Calls the SuperBowlbutton function that display a button for user to press to if the team has won a SuperBowl. 
Superbowlbutton()

## Filtering By Season Section 
st.subheader(f'View {selected} By Season')

# creates a drop down box for users to select which season they would like to examine.  
selectedseason = st.selectbox("Select a Season", season)

# Calls the infobyYear function and creates variables that contain data for selected team and season.
r, PassingYds =infobyYear(data, selected, selectedseason)

# Call the rushingvsPassingchart function that display a pie chart of the rushing vs passing yard for the team that season.
st.pyplot(rushingvsPassingchart(r,PassingYds))

## Offense VS. Defense Section 
st.header(f'Top 10 Offense VS. Defense From {selectedseason} Season')

# Create buttons to display the Top 10 Offensives or Defensives for the selected season. 
offenseTopTen = st.checkbox("Top 10 Offensives this Season", False)
DefenseTopTEN =st.checkbox("Top 10 Defensives this Season", False)

# Run through the situations of checkboxes above and when should display certain data. 
if offenseTopTen and DefenseTopTEN:
    offenseTopTen = OFcomparison10byseason(data, selectedseason)
    DefenseTopTEN = DEcomparison10byseason(df5, selectedseason)
elif offenseTopTen:
    OFcomparison10byseason(data, selectedseason)
elif DefenseTopTEN:
    DefenseTopTEN = DEcomparison10byseason(df5, selectedseason)
else:
    " "
## SuperBowl Champs Section   
st.header(f'{selectedseason} Season: SuperBowl Champions')

# Call the superbowlchampbyseason function that display the SuperBowl champions for the selected season. 
superbowlchampbyseason(data,df5,selectedseason)