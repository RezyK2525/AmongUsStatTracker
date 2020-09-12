# AmongUsStatTracker Discord Bot
inite like to try out bot    https://discord.com/oauth2/authorize?client_id=753339077880971385&permissions=8&scope=bot
Our bot is a simple easy way to both keep track of overall and daily w/l data for games of AmongUs
We first have all players initialize themselves into a database where the data is later stored using the .create command
once all the players succesfully join they will never have to use the create command again.
now when you go to play the game you use the .join command.
when you are finished playing use the .leave command
.join will put all of the current players into an array that is used to update specific players stats based on who is actually in the game
finally after everygame in order to update all of the players stats you use the .update command.

Command Syntax
.create @yourself username       (Initializes you into the database, REQUIRED to have stats with this bot)
.join @yourself    (Joins the current game) 
.leave @yourself     (Leaves the current game)
.clear    (Clears everyone in the game and also clears the daily stat table)
.update @imposter1 @imposter2 w/l  (this will update everyone in the games stats)
.stats @yourself or @someoneelse  (Will pull up that persons individual stats)
.stats game      (Will pull everyones stats currently playing the game)
.daily @yourself or @someoneelse  (Will pull up that persons individual daily stats)
.daily game      (Will pull everyones daily stats currently playing the game)
