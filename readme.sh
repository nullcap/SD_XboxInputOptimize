i# Steam Deck Xbox Controller Bluetooth Configuration Script

This Python script helps you configure the connection parameters for Xbox controllers connected to your Steam Deck via Bluetooth, reducing input lag. It searches for connected Xbox controllers and updates the \`/var/lib/bluetooth/$bluetooth_controller/$bluetooth_device/info\` file with the specified connection parameters.

## Warnings

- The script must be run with root privileges (use \`sudo\`).
- This script may introduce issues and comes with no warranties. Use at your own risk.

## Usage

1. Save the script to a file called \`xbox_bluetooth_config.py\`.

2. Run the script with root privileges:

\`\`\`bash
sudo python3 xbox_bluetooth_config.py
\`\`\`

3. Follow the prompts to configure the Xbox controller(s) or choose another Bluetooth device to configure.

4. Optionally, restart the Bluetooth service when prompted to apply the changes.

5. To restore a previous configuration from a backup, run the script again and choose the restore option when prompted.

## Example

\`\`\`
$ sudo python3 xbox_bluetooth_config.py
WARNING: This script may introduce issues and comes with no warranties.
Type 'yes' to confirm you understand: yes
Do you want to restore the configuration from a backup? [y/N]: N
Found Xbox controller(s):
  /var/lib/bluetooth/AA:BB:CC:DD:EE:FF/11:22:33:44:55:66/info
Do you want to configure the found Xbox controller(s)? [Y/n]: Y
Do you want to restart the Bluetooth service after updating the configuration? [Y/n]: Y
Configuration file backed up to: 11:22:33:44:55:66_backup_20230401_103515.info
Bluetooth configuration updated successfully
\`\`\`

## Reference

This script was inspired by the following Reddit post:

[Reducing input lag when using Xbox controller on Steam Deck](https://www.reddit.com/r/SteamDeck/comments/vu53p9/reducing_input_lag_when_using_xbox_controller/)

## Author

This script and README were entirely written by ChatGPT, an AI language model by OpenAI.


