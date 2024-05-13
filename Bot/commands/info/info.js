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
		let validInteraction = interaction;
		const type = interaction.options.getString('info');
		var response = '';
        let warningEmbed = '';

        try {
            if (type === 'version') {
                response = '1.0.0';
            }
            else if (type === 'author') {
                response = '[TheOfficialPeter](https://github.com/theofficialpeter)';
            }
            else if (type === 'servercount') {
                response = interaction.guild.memberCount;
            }
            else if (type === 'payment') {
                response = 'No payment options as of yet!';
            }
            else if (type === 'about') {
                response = "Welcome to Fruno 1.0 The best linux gaming companion. With a ton of features to help you get the most out of your gaming experience."
            }

            if (response === 'Invalid information type') {
                interaction.reply('No information found for the selected option. Please try again.');
            }
            else if (response === '') {
                interaction.reply('No information found for the selected option. Please try again.');
            }
            else {
                const infoEmbed = new EmbedBuilder()
                    .setColor('#0099FF')
                    .setTitle('Information')
                    .setDescription('Here is the information you requested:')
                    .addFields(
                        { name: 'Requested Information', value: String(response) }, // Convert response to a string
                        { name: '🔍 Type', value: type }
                    )
                    .setTimestamp()
                    .setFooter({ text: 'Requested by: ' + interaction.user.tag });

                validInteraction.channel.send({ embeds: [infoEmbed] });
            }
        } catch (error) {
            console.error('Error processing interaction:', error);
            return;
        }
	},
};

