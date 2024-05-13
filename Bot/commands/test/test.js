const { EmbedBuilder } = require('discord.js');
const { SlashCommandBuilder } = require('@discordjs/builders');

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
		var response = '';

		if (type === 'ping') {
			response = await fetch('https://api.foxwire121.workers.dev');
		}
		else if (type === 'api') {
			response = await fetch('https://api.foxwire121.workers.dev/fetch?name=astroneer');
		}
		else {
			response = 'Invalid test type';
		}

		if (response === 'Invalid test type') {
			var warningEmbed = new EmbedBuilder()
				.setColor('#ff0000')
				.setTitle(':x: Invalid Test Type')
				.setDescription('The test type you have entered is invalid. Please try again with a valid test type.')
				.setTimestamp()
				.setFooter({ text: "~ Made by theofficialpeter" });
		}
		else if (response === '') {
			var warningEmbed = new EmbedBuilder()
				.setColor('#ff0000')
				.setTitle(':x: API Offline Warning')
				.setDescription('The API is currently offline. Please wait for an update from the developers.')
				.addFields({ name: 'API Response', value: ` \`\`\` ${await response.text()} \`\`\` ` },
						{ name: "Urgency", value: "High" },
						{ name: "Recommended Actions", value: "Wait for fix from developers"},
						{ name: "ETA Fix", value: "3 Hours"})
				.setTimestamp()
				.setFooter({ text: "~ Made by theofficialpeter" });
		}
		else {
			var warningEmbed = new EmbedBuilder()
				.setColor('#ff0000')
				.setTitle(':x: API Offline Warning')
				.setDescription('The API is currently offline. Please wait for an update from the developers.')
				.addFields({ name: 'API Response', value: ` \`\`\` ${await response.text()} \`\`\` ` },
						{ name: "Urgency", value: "High" },
						{ name: "Recommended Actions", value: "Wait for fix from developers"},
						{ name: "ETA Fix", value: "3 Hours"})
				.setTimestamp()
				.setFooter({ text: "~ Made by theofficialpeter" });
			interaction.reply({ embeds: [warningEmbed] });
		}
        
		if (warningEmbed === '') {
			interaction.channel.send({ embeds: [warningEmbed] });
		}
		else {
			interaction.channel.send("Something went wrong. Please try again later.");
		}
	},
};

