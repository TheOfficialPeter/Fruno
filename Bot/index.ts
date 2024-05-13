// import discord.js
const { Client, Collection, Events, GatewayIntentBits } = require('discord.js');
const path = require('node:path');
import { type Interaction, type Client as ClientType, EmbedBuilder } from 'discord.js';
import fs from 'fs';
const tokenData = require('./config.json');
const fetch = require('node-fetch');
const cron = require('node-cron');

const client = new Client({intents: [GatewayIntentBits.Guilds]});
client.commands = new Collection();

const loadCommands = () => {
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
            if ('data' in command && 'execute' in command) {
                client.commands.set(command.data.name, command);
            } else {
                console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
            }
        }
    }
};

const handleInteraction = async (interaction: Interaction) => {
    if (!interaction.isCommand()) return;

    const command = client.commands.get(interaction.commandName);

    if (!command) {
        console.error(`No command matching ${interaction.commandName} was found.`);
        return;
    }

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        const errorMessage = 'There was an error while executing this command!';
        if (interaction.replied || interaction.deferred) {
            await interaction.followUp({ content: errorMessage, ephemeral: true });
        } else {
            await interaction.reply({ content: errorMessage, ephemeral: true });
        }
    }
};

client.on(Events.InteractionCreate, handleInteraction);

client.once(Events.ClientReady, (c: ClientType) => {
    console.log(`Ready! Logged in as ${c.user?.tag}`);

    cron.schedule('*/10 * * * *', async () => {
        try {
            const response = await fetch('https://api.foxwire121.workers.dev');
            if (!response.ok) {
                const channel = client.channels.cache.get('1239591848415330357');
                if (channel) {
                    const warningEmbed = new EmbedBuilder()
                        .setColor('#ff0000')
                        .setTitle('API Offline Warning')
                        .setDescription('The API is currently offline. Please wait for an update from the developers.')
                        .addFields({ name: 'API Response', value: `\`\`\`${response}\`\`\`` });

                    channel.send({ embeds: [warningEmbed] });
                }
            }
        } catch (error) {
            console.error('Error checking API status:', error);
        }
    });
});

const login = () => {
    client.login(tokenData.token);
};

loadCommands();
login();