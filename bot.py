import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from rag import send_to_chatGpt

load_dotenv(override=True)

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'we have logged in as {client.user.name}')

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="GUEST")
    if role:
        try:
            await member.add_roles(role)
            print(f"Assigned role {role.name} to {member.name}")
        except discord.Forbidden:
            print("I don't have permission to assign roles.")
        except discord.HTTPException as e:
            print(f"Failed to assign role: {e}")

            
    channel = client.get_channel(1288484073106575453)
    if channel:
        await channel.send(
                            "BLISS에 오신 것을 환영합니다.\n"
                            "신입 안내 드리겠습니다.\n\n"
                            "1. 7일간은 테스트 기한입니다. 일주일간 룰 위반 없이 6시간 이상 클랜에서 플레이 부탁드립니다. (정회원 등업 후에는 2주 기준 6시간입니다.)\n\n"
                            "2. 일주일 후 배린이로 승급됩니다. DM 확인 부탁드립니다.\n\n"
                            "3. 가입 후 게임은 즉시 가능합니다. @here 명령어를 사용하여 일반 천국 및 경쟁 천국에서 구인하시거나 남는 방에 들어가 주세요.\n\n"
                            "4. 정회원 등업 후 인게임 클랜 가입, 교류 클랜 입장 및 지인 초대가 가능합니다.\n\n"
                            "5. 클랜에 문의사항이 있을 경우, 양식 모음 채널에 들어가서 양식을 복사한 후 작성하여 운영진 마끼야또님께 DM으로 문의 부탁드립니다. (다른 분을 대신해서 문의하지 말아주세요.)\n\n"
                            "6. 인게임 닉변은 자유입니다.\n\n"
                            "7. 이중 클랜은 금지입니다. 단, 배그 공식 디스코드 서버 같은 공방 서버에서 플레이는 가능합니다.\n"
                        )
        
        dm_channel = await member.create_dm()  # DM 채널 생성
        
        await dm_channel.send(
                            "먼저, 아래 링크를 클릭하여 클랜 마크 채널로 이동하세요:\n"
                            "https://discord.com/channels/913444484967202858/1004373114924302377\n\n"
                            "해당 채널에서 신입 마크를 다운로드한 후, 그 마크로 디스코드 프로필 사진을 변경해 주세요.\n\n"
                            "서버 닉네임을 '별명/나이' 형식으로 변경해 주세요. 예: 코카/31\n"
                            "(나이는 만 나이가 아닌 실제 나이로 기재해 주세요.)\n\n"
                        )
        
        await dm_channel.send(
                            "그 다음, 아래 링크를 클릭하여 자기소개 채널로 이동하세요:\n"
                            "https://discord.com/channels/913444484967202858/913469232887504936\n\n"
                            "채널에 들어가시면 상단에 있는 자기소개 양식을 복사한 후, 간단한 자기소개서를 작성해 주세요.\n\n"
                            "민감한 개인 정보는 포함되지 않으며, 가입 날짜 기록과 홍보글 출처를 확인하기 위한 용도입니다.\n"
                            "개인적인 용도로 사용되지 않으니 안심하세요.\n\n"
                            )

        await dm_channel.send(
                            "마지막으로, 아래 링크를 클릭하시면 BLISS 룰이 있는 채널로 이동됩니다:\n"
                            "https://discord.com/channels/913444484967202858/913496734863360020\n\n"
                            "이곳에서 규칙 10가지를 읽어주시기 바랍니다.\n"
                            "모든 과정을 완료하셨다면 확인이라고 가입문의방에 입력해주세요\n"
                            "바로 클랜에 대한 추가 안내 및 등업을 도와드리겠습니다.\n\n"
                            "BLISS에 오신 것을 환영합니다! 여기서 즐겁게 게임하시고 잘 지내시길 바랍니다~"
                        )


@client.command()
async def gpt(ctx, *, message):
    
    if message.startswith("확인"):
        await ctx.send("""BLISS에 오신것을환영합니다\n 여기서 즐겁게 게임하시고\n 잘지내시길 바라겠습니다~""")
        role = discord.utils.get(ctx.guild.roles, name="배생아")
        remove_role = discord.utils.get(ctx.guild.roles, name="GUEST")
        if role:
            try:
                await ctx.author.add_roles(role)
                print(f"Assigned role {role.name} to {ctx.author.name}")
            except discord.Forbidden:
                print("I don't have permission to assign roles.")
            except discord.HTTPException as e:
                print(f"Failed to assign role: {e}")

        if remove_role:
            try:
                await ctx.author.remove_roles(remove_role)
                print(f"remove role {remove_role.name} to {ctx.author.name}")
            except discord.Forbidden:
                print("I don't have permission to remove roles.")
            except discord.HTTPException as e:
                print(f"Failed to remove role: {e}")

    elif message.strip():        
        #OpenAI API가 대답
        response = send_to_chatGpt(message)
        # Send the response as a message
        await ctx.send(response)


client.run(TOKEN)