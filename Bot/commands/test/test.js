const { SlashCommandBuilder } = require('@discordjs/builders');
const { EmbedBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('test')
		.setDescription('Run a live test on the online API')
		.addStringOption(option =>
			option.setName('type')
			.setDescription('The type of test to run')
			.addChoices(
				{ name: 'ping', value: 'ping' },
				{ name: 'api', value: 'api' }
			)
		),
	async execute(interaction) {
		const type = interaction.options.getString('type');
		let response = '';

		if (type === 'ping') {
			response = await fetch('https://api.foxwire121.workers.dev');
		}
		else if (type === 'api') {
			response = await fetch('https://api.foxwire121.workers.dev/fetch?name=astroneer');
		}
		else {
			response = 'Invalid test type';
		}

		let warningEmbed = new EmbedBuilder()
			.setColor('#ff0000')
			.setTitle(response === 'Invalid test type' ? ':x: Invalid Test Type' : ':x: API Offline Warning')
			.setDescription(response === 'Invalid test type' ? 'The test type you have entered is invalid. Please try again with a valid test type.' : 'The API is currently offline. Please wait for an update from the developers.')
			.setTimestamp()
			.setFooter({ text: "~ Made by theofficialpeter" });

		if (response === '') {
			warningEmbed.addFields({ name: 'API Response', value: ` \`\`\` ${await response.text()} \`\`\` ` },
				{ name: "Urgency", value: "High" },
				{ name: "Recommended Actions", value: "Wait for fix from developers" },
				{ name: "ETA Fix", value: "3 Hours" });
		}

		if (response === 'Invalid test type' || response === '') {
			interaction.channel.send({ embeds: [warningEmbed] });
		} else {
			interaction.channel.send("Something went wrong. Please try again later.");
		}
	},
};
