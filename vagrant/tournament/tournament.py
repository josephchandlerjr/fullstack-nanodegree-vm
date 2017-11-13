#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect();
    cur = conn.cursor();
    cur.execute("delete from match;")
    cur.execute("update record set win = 0, loss = 0;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect();
    cur = conn.cursor();
    deleteMatches()
    cur.execute("delete from record;")
    cur.execute("delete from player;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect();
    cur = conn.cursor();
    cur.execute("select count(*) from player;")
    result = cur.fetchone()
    conn.close()
    return result[0]
   


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = bleach.clean(name)
    conn = connect();
    cur = conn.cursor();
    cur.execute("insert into player values (%s)", (name,))
    conn.commit()
    cur.execute("select max(id) from player;")
    recently_added_id = cur.fetchall()[0]
    cur.execute("insert into record values (%s, 0, 0);", (recently_added_id,))
    conn.commit()
    conn.close()
   

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""select record.id, 
                   player.name, 
                   record.win, 
                   (record.win + record.loss) as matches
                 from record, player
                 where record.id = player.id
                 order by record.win desc;""")
    result = cur.fetchall()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into match values (%s, %s);", (winner,loser))
    cur.execute("update record set win = win + 1 where id = %s;", (winner,))
    cur.execute("update record set loss = loss + 1 where id = %s;", (loser,))
    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    standings = playerStandings()
    for i in range(0,len(standings)-1, 2):
        pairings = pairings + [(standings[0][0],standings[0][1],standings[1][0],standings[1][1])]
    return pairings 


