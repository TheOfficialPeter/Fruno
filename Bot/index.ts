// import discord.js
const { Client, Collection, Events, GatewayIntentBits } = require('discord.js');
const path = require('node:path');
import type { Interaction, Client as ClientType } from 'discord.js';
import fs from 'fs';
const tokenData = require('./config.json');
const fetch = require('node-fetch');
const cron = require('node-cron');

const client = new Client({intents: [GatewayIntentBits.Guilds]});
client.commands = new Collection();

const foldersPath = path.join(__dirname, 'commands');
console.log("Folders path: " + foldersPath);
const commandFolders = fs.readdirSync(foldersPath);

for (const folder of commandFolders) {
	const commandsPath = path.join(foldersPath, folder);
    console.log("Command path: " + commandsPath);
	const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));
	for (const file of commandFiles) {
		const filePath = path.join(commandsPath, file);
		const command = require(filePath);
		// Set a new item in the Collection with the key as the command name and the value as the exported module
		if ('data' in command && 'execute' in command) {
			client.commands.set(command.data.name, command);
		} else {
			console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
		}
	}
}

client.on(Events.InteractionCreate, async (interaction: Interaction) => {
	if (!interaction.isChatInputCommand()) return;

	const command = client.commands.get(interaction.commandName);

	if (!command) {
		console.error(`No command matching ${interaction.commandName} was found.`);
		return;
	}

	try {
		await command.execute(interaction);
	} catch (error) {
		console.error(error);
		if (interaction.replied || interaction.deferred) {
			await interaction.followUp({ content: 'There was an error while executing this command!', ephemeral: true });
		} else {
			await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
		}
	}
});

client.once(Events.ClientReady, (c: ClientType) => {
    console.log(`Ready! Logged in as ${c.user?.tag}`);
    
    cron.schedule('*/10 * * * *', async () => {
        try {
            const response = await fetch('https://api.foxwire121.workers.dev');
            if (!response.ok) {
                const channel = client.channels.cache.get('1239591848415330357');
                if (channel) {
                    const warningEmbed = new client.discord.MessageEmbed()
                        .setColor('#ff0000')
                        .setTitle('API Offline Warning')
                        .setDescription('The API is currently offline. Please wait for an update from the developers.')
                        .addField('API Response', `\`\`\`${response}\`\`\``);
                    
                    channel.send({ embeds: [warningEmbed] });
                }
            }
        } catch (error) {
            console.error('Error checking API status:', error);
        }
    });
});

// Load Discord token from a JSON file instead of using process.env.DISCORD_TOKEN
client.login(tokenData.token);
