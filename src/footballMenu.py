# Football menu system

import football as fb
import pprint
import commonFunctions as cf

__author__ = "David Bristoll"
__copyright__ = "Copyright 2018, David Bristoll"
__maintainer__ = "David Bristoll"
__email__ = "david.bristoll@gmail.com"
__status__ = "Development"

# temporary, placeholder functions:

def analyse_fixtures(x):
    print("\nThe analyse fixtures feature is not yet available.\n")

def single_game_analysis(x):
    print("\nThe single game analysis feature is not yet available.\n")

def leave(x):
    print("\nExit to previous menu.\n")


def choose_leagues(league_data, fixtures, data_source):
    #league_data_and_fixtures = 
    fb.select_league(league_data, fixtures, data_source)
    #league_data = league_data_and_fixtures[0]
    #fixtures = league_data_and_fixtures[1]

def display_selected_leagues(league_data):
    pprint.pprint(league_data)

def display_fixtures(fixtures):
    """
    Takes in the current list of fixtures (each fixture being a list of 4 items).
    
    Displays the list on the screen.
    """
    for fixture in fixtures:
        for detail in range(4):
            print(fixture[detail] + " ", end = " ")
        print("")
    return 0


def display_predictions(predictions):
    """
    Takes in the current list of predictions generated via game analysis options.
    Displays the predictions on screen.
    """

    if not predictions:
        print("\nNo predictions to display. Run manual game analysis and select games to predict first.")

        print("\nPress enter to return to previous menu.")
        input()
        return
    else:
        print("\nPredictions")
        print("===========")
        league = ""
        for game in predictions:
            # If a new league is present, print the league name
            if game["League"] != league:
                print("\n\n" + game["League"] + "\n")
            league = game["League"]
            print(game["Date"], game["Time"], game["Home team"], game["Home team prediction"], game["Away team"], game["Away team prediction"])
            
        print("\nPress enter to return to previous menu.")
        input()
        return


def reports(league_data, fixtures, predictions):
    print("\nReports Menu")
    print("============")
    
    report_options = [["(1) Export league data (!fixture information not currently included!)", "1"],
                      ["(2) Display currently loaded league data", "2"],
                      ["(3) Display currently loaded fixtures", "3"],
                      ["(4) Display predictions", "4"],
                      ["(5) Save predictions to file", "5"],
                      ["(M) Return to previous menu", "m"]
                      ]
    
    exit_menu = False
    available_options = []
    selection = ""
    
    # Gather a list of available_option numbers for input recognition

    for option in report_options:
        available_options.append(option[1])
    
    while not exit_menu:
        
        selected_leagues = []
        
        for option in report_options:
            print(option[0])
            
        while selection not in available_options:
            selection = input()
            selection = selection.lower()
        
        # Menu selection conditionals
        if selection.lower() == "m":
                exit_menu = True
                return league_data
        if selection == report_options[0][1]: # Export league data to JSON
            cf.export_data(league_data, "json")
        if selection == report_options[1][1]: # Display currently loaded league data
            display_selected_leagues(league_data)
        if selection == report_options[2][1]: # Display currently loaded fixtures
            display_fixtures(fixtures)     
        if selection == report_options[3][1]: # Display currently loaded predictions
            display_predictions(predictions)
        if selection == report_options[4][1]: # Save predictions
            if predictions:
                cf.export_data(fb.prepare_prediction_dataframe(predictions), "xls")
            else:
                print("\nNo predictions loaded. Generate predictions or run game analysis first.\n")
        selection = ""


def football_menu(league_data, fixtures, predictions):
    data_source = "Soccer Stats"
    football_options = [["(1) Select a league", "1", choose_leagues],  # The selectLeague function from football.py
                        ["(2) Generate predictions on currently loaded fixtures", "2"],
                        ["(3) Single game analysis from fixture list*", "3", single_game_analysis],
                        ["(4) Manual single game analysis", "4", fb.manual_game_analysis],
                        ["(5) Reports", "5", reports],
                        ["(6) Import data from JSON file", "6"],
                        ["(7) Clear currently loaded league data", "7"],
                        ["(8) Clear currently stored prediction data", "8"],
                        ["(9) Change data source (CLEARS ALL DATA)", "9"],
                        ["(Q) Quit", "q", leave]
                        ]
    
    # ["(M) Previous menu", "m", leave] - removed as prev menu currently bypassed
    selected_leagues = []
    exit_menu = False
    available_options = []
    selection = ""

    # Gather a list of availableOption numbers for input recognition
    for option in football_options:
        available_options.append(option[1])
    
    while not exit_menu:
        if league_data == {}:
            football_options[0][0] = "(1) Select a league"
        else:
            football_options[0][0] = "(1) Select another league"
        
        selected_leagues = []

        #  If there are leagues selected in LeagueData, add them to the selectedLeagues
        #  list and display the list.
        if league_data != {}:
            for league in league_data:
                selected_leagues.append(league)
            print("\n Selected league(s):\n")
            for league in selected_leagues:

                print(league)
            print()
        else:
            print("\nNo league currently selected. Please start by selecting a league.\n")

        print("Currently selected data source: " + data_source + "\n")
        # Display the available options

        for option in football_options:

            print(option[0])
            
        # Display any additional information
        print("\nItems marked with a * are not available in this version.")

        # Keep asking for a selection while the selection provided is not in the availableOptions list.
        while selection not in available_options:
            selection = input().lower()

        # If the selection is in the list, run it's function passing
        # the leagueData dictionary by default.
        for option in football_options:
            """if selection == "m":
                exit_menu = True
                break           
                continue """ #Commented out as previous menu bypassed.
            if selection == "q":
                quit()
            if selection == "1": # Select league
                choose_leagues(league_data, fixtures, data_source)
                selection = ""
                continue
            if selection == "2": # Run analysis on currently loaded fixtures
                predictions = fb.upcoming_fixture_predictions(fixtures, predictions, league_data)
                selection = ""
                continue
            if selection == "4": # Manual single game analysis
                exit_manual_analysis_menu = False
                while not exit_manual_analysis_menu:
                    selection = ""
                    another_game = ""
                    
                    # Manual_predictions holds an error message if something goes wrong.
                    manual_predictions = fb.manual_game_analysis(league_data, predictions) 
                    while another_game.lower() != "y" and another_game.lower() != "n":
                    
                        # If something went wrong, don't ask to run another game analysis.
                        print(manual_predictions)
                        if manual_predictions == "No leagues loaded":
                            exit_manual_analysis_menu = True
                            break
                        else:
                            print("\nAnalyse another game? (Y/N)")
                            another_game = input()
                        if another_game.lower() == "n":
                            exit_manual_analysis_menu = True
                            break
                        if another_game.lower() == "y":
                            break
                                
            if selection == "5": # Reports
                reports(league_data, fixtures, predictions)
                selection = ""
                continue
            if selection == "6": # Import data from JSON file
                new_data = cf.import_json_file()
                if new_data == None: # If load fails
                    del new_data
                else:
                    league_data = new_data.copy()
                    del new_data
                selection = ""
                continue
            if selection == "7": # Clear currently loaded league data.
                league_data = {}
                fixtures = []
                selection = ""
                continue    
            if selection == "8": # Clear currently loaded predictions data.
                predictions.clear()
                selection = ""
                continue
            if selection == "9": # Switch data source.
                if data_source == "Soccer Stats":
                    data_source = "Bet Study"
                else:
                    data_source = "Soccer Stats"
                league_data = {}
                fixtures = []
                predictions.clear()
                selection = ""
                continue
                
            # General action for other menu items
            if selection == option[1]:
                option[2](league_data)
                selection = ""
                continue
