import sys
import mysql.connector
from mysql.connector import Error
import blackjack_game
import player


""" --- Database definitions --- """

def create_connection(host_name, user_name, user_password):
    """ Establish a connection to the server """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            )
        print("Connection to MySQL DB successful")
    except Error as e:
        print("The error {} occured".format(e))
        exit()
    return connection


def join_connection_and_DB(host_name, user_name, user_password, db_name):
    """ Join the connection and the desired database """
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
            )
        print("Join of connection and database successful")
    except Error as e:
        print("The error {} occured".format(e))
        exit()
    return connection


def create_database(connection, query):
    """ Establish a new database """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print("The error {} occured".format(e))
        exit()


def execute_query(connection, query, param=None):
    """ Commitable queries for database"""
    cursor = connection.cursor()
    try:
        if(param):
            cursor.execute(query, param)
        else:
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print("The error {} occured".format(e))


def execute_read_query(connection, query, param=None): #edit for params
    """ Fetch data from the database """
    cursor = connection.cursor()
    result = None
    try:
        if param:
            cursor.execute(query, param)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print("The error {} occurred".format(e))


def make_tables():
    """ Create database tables """
    create_players_table = """
    CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT,
    name TEXT NOT NULL,
    score INT,
    PRIMARY KEY (id)
    ) ENGINE = InnoDB
    """
    execute_query(connection, create_players_table)

    # Create a table for qlearning agent (Not used yet)
    create_hand_table = """
    CREATE TABLE IF NOT EXISTS hands (
    id INT AUTO_INCREMENT,
    card_one TEXT NOT NULL,
    card_two TEXT NOT NULL,
    win_probability FLOAT,
    reward UNSIGNED INT,
    player_id INTEGER NOT NULL,
    FOREIGN KEY fk_player_id (player_id) REFERENCES players(id),
    PRIMARY KEY (id)
    ) ENGINE = InnoDB
    """
    #execute_query(connection, create_hand_table)



def reset_player_table():
    """ Resets the player table for a new batch """
    execute_query(connection, "DELETE from players")
    execute_query(connection, "ALTER TABLE players AUTO_INCREMENT=1")



""" --- Start of main for black jack game --- """

if __name__ == '__main__':
    # Make the initial connection using the above function
    connection = create_connection("localhost","root",sys.argv[1])
    # Create the database with the established connection
    create_database_query = "CREATE DATABASE IF NOT EXISTS blakjack"
    create_database(connection, create_database_query)
    #update connection to use the newly made DB
    connection = join_connection_and_DB("localhost","root",sys.argv[1], "blakjack")
    make_tables()
    reset_player_table() # reset everytime until building game history
    people = ['Dealer'] + sys.argv[2:]
    players = [] # players are people with cards
    for p in people: # deal the cards to the players, add players to DB
        query = "INSERT INTO players (name, score) VALUES (%s, %s)"
        execute_query(connection, query, (p, 0)) # initial $ or win margin?
        players.append(player.player(p))
    print("Starting Game...\n")
    print("==== Black Jack ====\n")

    # Play four games. Only one deck. (only one for now)
    for i in range(0,1):
        game = blackjack_game.blackjack_game(players)
        result = game.begin_game()
        score_query = "SELECT score FROM players WHERE name = %s"
        player_score = int(execute_read_query(connection,
                            score_query, (result.name,))[0][0])
        query = "UPDATE players SET score=(%s) WHERE name=(%s)"
        execute_query(connection, query, (player_score+game.pot, result.name))
        print("{} won ${} with the hand {}".format(
                result.name, game.pot, result.hand))

    winner_query = """SELECT name FROM players
                        WHERE score = (SELECT MAX(score) FROM players)"""
    winner = execute_read_query(connection,winner_query)
    print("\n::: The Winner Of the Table Is {} :::".format(winner[0][0]))
    print("\n---------------------------------")
    print("|         End of Game           |")
    print("---------------------------------\n")


# Close properly
connection.close()
