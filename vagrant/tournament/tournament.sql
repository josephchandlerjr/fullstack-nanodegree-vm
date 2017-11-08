-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (name text,
                      id serial primary key);

create table record (id integer references players,
                     win integer,
                     loss integer); 

create table matches (player1 integer references players (id), 
                      player2 integer references players (id), 
                      round_num integer,
                      winner integer references players (id)
                      );

