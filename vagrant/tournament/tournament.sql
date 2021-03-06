-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table player (name text,
                      id serial primary key);

create table record (id integer references player,
                     win integer,
                     loss integer); 

create table match (winner integer references player (id), 
                      loser integer references player (id) );

