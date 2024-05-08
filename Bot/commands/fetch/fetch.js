const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('fetch')
		.setDescription('Fetches Game Info + Analytics + Download Links')
        .addStringOption(option =>
            option.setName('name')
                .setRequired(true)
                .setDescription('The name of the game to fetch')),
	async execute(interaction) {
        const msg = interaction.options.getString('name');
        if (msg) {
            await interaction.reply(msg);
        } else {
            await interaction.reply('You didn\'t provide any input!');
        }
	},
};