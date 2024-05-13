const { EmbedBuilder } = require('discord.js');
const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('fetch')
		.setDescription('Fetches Game Information, Analytics, and Media')
        .addStringOption(option =>
            option.setName('name')
                .setRequired(true)
                .setDescription('Enter the name of the game to fetch')),
	async execute(interaction) {
        const msg = interaction.options.getString('name');
        if (msg && msg != '') {
            var response = await fetch(`https://api.foxwire121.workers.dev/fetch?name=${msg}`);
            response = await response.json();

            const gameInfo = {
                name: response.name,
                userScore: response.userScore,
                tier: response.tier,
                gameId: response.gameId,
            };

            const embed = new EmbedBuilder()
                .setColor(0x0099FF)
                .setTitle(gameInfo.name)
                .setURL('https://discord.js.org/')
                .setAuthor({ name: 'Some name', iconURL: 'https://i.imgur.com/AfFp7pu.png', url: 'https://discord.js.org' })
                .setDescription('Game Description goes here')
                .setThumbnail('https://i.imgur.com/AfFp7pu.png')
                .addFields(
                    { name: 'Game User Rating', value: gameInfo.userScore.toString() },
                    { name: 'Linux Compatibility Tier', value: gameInfo.tier.toString() },
                    { name: 'Game ID', value: gameInfo.gameId.toString() },
                    { name: 'Testing this shit bruh', value: 'Some fucked up value here' }
                )
                .setImage('https://i.imgur.com/AfFp7pu.png')
                .setTimestamp()
                .setFooter({ text: 'Fetched using Fruno Bot', iconURL: 'https://github.com/theofficialpeter/fruno' });
                
            await interaction.reply({ embeds: [embed] });
        } else {
            await interaction.reply('You didn\'t provide any input!');
        }
	},
};
