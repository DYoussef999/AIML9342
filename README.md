This is a Discord recommendation bot made during an Artificial Intelligence and Machine Learning (AIML9342) course offered jointly by the University of Toronto & Circuit Stream. 
- Connects to Discord using a token from a .env file.
- Responds to specific user commands like !hi, !bye, !roll, !flip, and rock-paper-scissors games (!rpsR, !rpsP, !rpsS).
- On !recommend, reads movie ratings from my_movies.csv, sends them to OpenAI's API, and replies with a movie recommendation. (can also do so based on large movie metadata files)
- Uses OpenAI's API to generate responses via a specific assistant.
NOTE: Discord bot token, OpenAI API key, and OpenAI assistant ID are all required.
