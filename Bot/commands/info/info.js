const { EmbedBuilder } = require('discord.js');
const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('info')
		.setDescription('Get information about Fruno')
		.addStringOption(option =>
			option.setName('info')
			.setDescription('The type of information to get')
			.addChoices(
				{ name: 'version', value: 'version' },
				{ name: 'author', value: 'author' },
                { name: 'servercount', value: 'servercount' },
                { name: 'payment', value: 'payment' },
                { name: 'about', value: 'about' },
			)
		),
	async execute(interaction) {
		const type = interaction.options.getString('info');
		let response = '';
		
		switch (type) {
			case 'version':
				response = '1.0.0';
				break;
			case 'author':
				response = '[TheOfficialPeter](https://github.com/theofficialpeter)';
				break;
			case 'servercount':
				response = interaction.guild.memberCount;
				break;
			case 'payment':
				response = 'No payment options as of yet!';
				break;
			case 'about':
				response = "Welcome to Fruno 1.0 The best linux gaming companion. With a ton of features to help you get the most out of your gaming experience.";
				break;
			default:
				response = 'Invalid information type';
				break;
		}

		const infoEmbed = new EmbedBuilder()
			.setColor('#0099FF')
			.setTitle('Information')
			.setDescription('Here is the information you requested:')
			.addFields(
				{ name: 'Requested Information', value: String(response) },
				{ name: '🔍 Type', value: type }
			)
			.setTimestamp()
			.setFooter({ text: 'Requested by: ' + interaction.user.tag });

		await interaction.reply(response === 'Invalid information type' ? 'No information found for the selected option. Please try again.' : { embeds: [infoEmbed] });
	},
};

