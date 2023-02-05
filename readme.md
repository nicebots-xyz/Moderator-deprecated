# Moderator Bot
A Discord bot that uses Google's Perspective API to moderate chat.

## Getting Started
There are three ways to use the Moderator Bot:

### 1. Add the Bot to Your Server  
This is the simplest option - simply invite the bot to your Discord server by clicking [here](https://discord.com/api/oauth2/authorize?client_id=1071451913024974939&permissions=1377342450896&scope=bot). You will need to have administrator permissions on your server to use the bot.

### 2. Run with Docker
To run the bot using Docker, use the following command:

```bash
docker run -e DISCORD_TOKEN=<your_discord_token> -e PERSPECTIVE_API_KEY=<your_perspective_api_key> -d /path/to/your/data:/Moderator/data paillat/moderator:latest
```

### 3. Clone and Run on Your Machine  
To run the bot on your local machine, clone this repository at `/Paillat-Dev/Moderator` and create a `.env` file with the following two values:

```env
DISCORD_TOKEN=<your_discord_token>
PERSPECTIVE_API_KEY=<your_perspective_api_key>
```

Then run `main.py` to start the bot, but remember to install the required packages first with 
```bash
pip install -r requirements.txt.
```

Note: If you're not comfortable with any of the above steps, we recommend using option 1.

## Commands and Usage
The Moderator Bot has the following command:

```bash
/setthreshold 
```

This command allows you to set the threshold for each type of toxicity. The options for toxicity are:

- toxicity
- severe_toxicity
- identity_attack
- insult
- profanity
- threat
- sexually_explicit
- flirtation
- obscene
- spam

To use the `/setthreshold` command, you must have administrator permissions. If a value is not specified, the default threshold will be set to 0.40. You can view the current settings for your server by using the `/setthreshold` command without any options.

The other commands are:
- 

## Built With
- [Discord](https://discord.com) - Communication platform for communities
- [Google Perspective API](https://perspectiveapi.com) - API for monitoring online conversations for toxic behavior

## Authors
- Paillat-Dev - Initial work

## License

This project is licensed under the MIT License.