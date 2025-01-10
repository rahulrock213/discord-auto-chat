import os
import asyncio
import discord
from colorama import init, Fore, Style
import time

init(autoreset=True)

red = Fore.LIGHTRED_EX
blue = Fore.LIGHTBLUE_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
black = Fore.LIGHTBLACK_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL
magenta = Fore.LIGHTMAGENTA_EX

print(f'\n{blue}+-+  +-++------+   +-+   +-+  +-++------++-+  +-++------++-+  +-++------++-+{reset}')
print(f'{blue}                        Aethereal auto leveling discord{reset}')
print(f'{blue}+-+  +-++------+   +-+   +-+  +-++------++-+  +-++------++-+  +-++------++-+\n{reset}')

def load_tokens():
    tokens = []
    try:
        with open('token.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    tokens.append(line.strip())
            if tokens:
                print(f"{green}Berhasil memuat {len(tokens)} token dari token.txt{reset}")
            return tokens
    except FileNotFoundError:
        print(f"{red}File token.txt tidak ditemukan!{reset}")
        print(f"{yellow}Buat file token.txt dengan format:{reset}")
        print(f"{yellow}TOKEN1{reset}")
        print(f"{yellow}TOKEN2{reset}")
        print(f"{yellow}TOKEN3{reset}")
        exit(1)

class AccountConfig:
    def __init__(self, token, channel_id, message_count, message_delay):
        self.token = token
        self.channel_id = channel_id
        self.message_count = message_count
        self.message_delay = message_delay  # delay antara setiap pesan

mainMessages = [
    'Just checking in!',
    'Did anyone see the latest episode?',
    'What everyone up to today?',
    'Cant believe its already this late!',
    'Just finished my tasks, finally!',
    'This weather is something else...',
    'Anyone working on something interesting?',
    'Good morning, everyone!',
    'Time for a quick break, anyone else?',
    'Back to the grind.',
    'Anyone have any tips for leveling up faster?',
    'Just got back, what did I miss?',
    'Feeling motivated today!',
    'Lol, thats hilarious!',
    'Totally agree with you.',
    'Thinking about getting some coffee, brb.',
    'Anyone here into coding?',
    'Oh wow, didnt expect that!',
    'Taking things one step at a time.',
    'Almost there!',
    'Lets keep pushing forward!',
    'Just chilling here for a bit.',
    'Anyone have any weekend plans?',
    'Anyone tried that new game yet?',
    'Haha, I know right?',
    'Feels like time is flying by.',
    'Well, thats a surprise!',
    'Just here to chat and relax.',
    'Anyone else feeling productive today?',
    'Im here to keep you all company!',
    'Hope everyones doing well!',
    'Taking a quick break, needed it.',
    'Lets keep this chat alive!',
    'Anyone else here love a good challenge?',
    'Feels good to be part of this community.',
    'Enjoying the vibe here!',
    'Thinking of learning something new.',
    'Random question: Cats or dogs?',
    'Its always nice to chat with you all.',
    'That sounds awesome!',
    'Haha, love the energy here!',
    'Alright, time to focus!',
    'Whats everyone watching these days?',
    'Just a casual hello!',
    'Oops, wrong chat haha.',
    'Wondering if anyone has advice on leveling?',
    'Anyone working late tonight?',
    'Hey, Im back!',
    'Hope I didnt miss too much.',
    'Alright, lets do this!',
    'Trying to stay motivated!',
    'Hows everyone feeling today?',
    'Good vibes only!',
    'Just saw something really cool!'
]

class Main(discord.Client):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    async def on_ready(self):
        print(f'{white}\nLogged in as {self.user}.{reset}')
        print(f'{green}Open the channel. . .{reset}')
        channel = self.get_channel(self.config.channel_id)
        
        if not channel:
            print(f'{red}Error: Channel tidak ditemukan!{reset}')
            await self.close()
            return
            
        sent_count = 0

        while sent_count < self.config.message_count:
            for i, msg in enumerate(mainMessages):
                if sent_count >= self.config.message_count:
                    break
                try:
                    sent_message = await channel.send(msg)
                    print(f'{green}[{self.user}] Sent message {sent_count+1} in #{channel.name}.{reset}')
                    
                    try:
                        await sent_message.delete()
                        print(f'{red}[{self.user}] Deleted message {sent_count+1} in #{channel.name}.{reset}')
                    except discord.errors.Forbidden:
                        print(f'{red}[{self.user}] Tidak bisa menghapus pesan (tidak ada izin){reset}')
                    except discord.errors.NotFound:
                        print(f'{red}[{self.user}] Pesan sudah dihapus{reset}')
                    
                    sent_count += 1
                    
                except discord.errors.Forbidden as e:
                    if "Cannot send messages in a voice channel" in str(e):
                        print(f'{red}Error: Tidak bisa mengirim pesan di voice channel!{reset}')
                        await self.close()
                        return
                    elif "slowmode" in str(e).lower():
                        print(f'{yellow}Channel dalam mode slowmode. Menunggu...{reset}')
                        await asyncio.sleep(10)  # Tunggu 10 detik jika kena slowmode
                        continue
                    elif "timeout" in str(e).lower():
                        print(f'{red}Error: Akun sedang dalam timeout!{reset}')
                        await self.close()
                        return
                    else:
                        print(f'{red}Error: Tidak bisa mengirim pesan! ({str(e)}){reset}')
                        await self.close()
                        return
                        
                except discord.errors.HTTPException as e:
                    if e.code == 429:  # Rate limit
                        retry_after = e.retry_after
                        print(f'{yellow}Rate limit terdeteksi. Menunggu {retry_after} detik...{reset}')
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        print(f'{red}Error HTTP: {str(e)}{reset}')
                        continue
                        
                except Exception as e:
                    print(f'{red}Error tidak dikenal: {str(e)}{reset}')
                    continue
                    
                await asyncio.sleep(self.config.message_delay)

        print(f'{yellow}[{self.user}] Completed sending {self.config.message_count} messages.{reset}')
        await self.close()

def main():
    print(f"{blue}Memuat token dari token.txt...{reset}")
    tokens = load_tokens()
    
    if not tokens:
        print(f"{red}Tidak ada token yang berhasil dimuat!{reset}")
        return
    
    channel_id = int(input(f"{magenta}Masukkan Channel ID: {reset}"))
    message_count = int(input(f"{magenta}Berapa banyak pesan yang akan dikirim: {reset}"))
    message_delay = int(input(f"{magenta}Delay antara setiap pesan (dalam detik): {reset}"))
    
    accounts = []
    for token in tokens:
        accounts.append(AccountConfig(token, channel_id, message_count, message_delay))
    
    # Menjalankan akun satu per satu
    for i, config in enumerate(accounts, 1):
        print(f"\n{blue}Menjalankan akun {i} dari {len(accounts)}...{reset}")
        try:
            # Buat event loop baru untuk setiap akun
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            client = Main(config)
            client.run(config.token, bot=False)
        except discord.LoginFailure:
            print(f'{red}Error: Token tidak valid atau expired!{reset}')
        except discord.PrivilegedIntentsRequired:
            print(f'{red}Error: Intents tidak diizinkan!{reset}')
        except Exception as e:
            print(f'{red}Error: {str(e)}{reset}')
        finally:
            # Pastikan event loop ditutup dengan benar
            try:
                loop.close()
            except:
                pass
            
        if i < len(accounts):  # Jika bukan akun terakhir
            print(f"{blue}Menunggu 5 detik sebelum menjalankan akun berikutnya...{reset}")
            time.sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{yellow}Program dihentikan oleh user{reset}")
    except Exception as e:
        print(f"\n{red}Terjadi error: {e}{reset}")
