from parsing import get_diet
import discord , asyncio , datetime , sys , os 
import parsing

def main():
    client = discord.Client()


    TOKEN = "NzE4ODY0MDg1MDkzMDU2NjEy.XtvEWQ.O21TX5txkHBfrsv4AQdbtwlN9aI"
    
    #명령어 목록
    Command_list = (
                    "```css\n"
                    "[NCC_bot Command List]\n"
                    "!도움말 - 도움말\n"
                    "!버전 - 버전 정보\n"
                    "!현재 시각 - 현재 시각을 알려줌\n"
                    "!급식 - 오늘 급식\n"
                    "!내일 급식 - 오늘 급식\n"
                    "!어제 급식 - 어제 급식\n"
                    "!내일모래 급식 - 내일모래 급식\n"
                    "!그저께 급식 - 그저께 급식\n"
                    "!식단 - 원하는 날의 급식 식단\n"
                    "```"
                    )
    #급식안내
    meal_notice = (
                    "```css\n"
                    "[-] 2019년 5월 2일 인 경우 19052 로 보낼 것.\n"
                    "[-] 2019년 10월 1일 인 경우 19101 로 보낼 것.\n"
                    "[-] 2020년 12월 7일 인 경우 20127 로 보낼 것.\n"
                    "[-] 2020년 5월 27일 인 경우 200527 로 보낼 것.\n"
                    "```"
                    )

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('---------')
        activity = discord.Game(name="!도움말을 눌러 도움말 확인하기")
        await client.change_presence(status=discord.Status.online, activity=activity)

    @client.event
    async def print_get_meal(local_date, local_weekday, message):
        l_diet = get_diet(2, local_date, local_weekday)
        d_diet = get_diet(3, local_date, local_weekday)

        if len(l_diet) == 1:
            embed = discord.Embed(title="No Meal", description="급식이 없습니다.", color=0x00ff00)
            await message.channel.send("급식이 없습니다", embed=embed)
        elif len(d_diet) == 1:
            lunch = local_date + " 중식\n" + l_diet
            embed = discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
            await message.channel.send("급식 정보입니다", embed=embed)
        else:
            lunch = local_date + " 중식\n" + l_diet
            dinner = local_date + " 석식\n" + d_diet
            embed= discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
            await message.channel.send("급식 정보입니다", embed=embed)
            embed = discord.Embed(title="Dinner", description=dinner, color=0x00ff00)
            await message.channel.send("급식 정보입니다", embed=embed)

    @client.event
    async def on_message(message):
        if message.content.startswith('!도움말'):
            await message.channel.send(Command_list)

        elif message.content.startswith('!버전'):
            embed = discord.Embed(title="Bot Version", description="updated", color=0x00ff00)
            embed.add_field(name="Version", value="2.0.0", inline=False)
            await message.channel.send("버전 정보입니다", embed=embed)

        elif message.content.startswith('!버젼'):
            embed = discord.Embed(title="Bot Version", description="updated", color=0x00ff00)
            embed.add_field(name="Version", value="2.0.0", inline=False)
            await message.channel.send("버전 정보입니다", embed=embed)

        elif message.content.startswith('!현재 시각'):
            dt = datetime.datetime.now()
            local_time = dt.strftime("%Y년 %m월 %d일 %H시 %M분 %S초".encode('unicode-escape').decode()).encode().decode('unicode-escape')
            embed = discord.Embed(title="Local Time", description=local_time, color=0x00ff00)
            await message.channel.send("현재 시각 정보입니다", embed=embed)

        elif message.content.startswith('!급식'):
            f_dt = datetime.datetime.today() + datetime.timedelta(days=0)
            meal_date = f_dt.strftime("%Y.%m.%d")
            whatday = f_dt.weekday()
            await print_get_meal(meal_date, whatday, message)

        elif message.content.startswith('!내일 급식'):
            f_dt = datetime.datetime.today() + datetime.timedelta(days=1)
            meal_date = f_dt.strftime("%Y.%m.%d")
            whatday = f_dt.weekday()
            await print_get_meal(meal_date, whatday, message)

        elif message.content.startswith('!어제 급식'):
            f_dt = datetime.datetime.today() + datetime.timedelta(days=-1)
            meal_date = f_dt.strftime("%Y.%m.%d")
            whatday = f_dt.weekday()
            await print_get_meal(meal_date, whatday, message)

        elif message.content.startswith('!그저께 급식'):
            f_dt = datetime.datetime.today() + datetime.timedelta(days=-2)
            meal_date = f_dt.strftime("%Y.%m.%d")
            whatday = f_dt.weekday()
            await print_get_meal(meal_date, whatday, message)

        elif message.content.startswith('!내일모래 급식'):
            f_dt = datetime.datetime.today() + datetime.timedelta(days=2)
            meal_date = f_dt.strftime("%Y.%m.%d")
            whatday = f_dt.weekday()
            await print_get_meal(meal_date, whatday, message)

        elif message.content.startswith('!식단'):
            request = meal_notice + '\n' + '날짜를 보내주세요...'
            request_e = discord.Embed(title="날짜를 보내주세요!", description=request, color=0xcceeff)
            await message.channel.send(message.channel, embed=request_e)
            meal_date = await client.wait_for('message', timeout=15.0)

            #입력이 없을 경우
            if meal_date is None:
                longtimemsg = discord.Embed(title="In 15sec", description='15초내로 입력해주세요. 다시시도 : !식단', color=0xff0000)
                await message.channel.send(message.channel, embed=longtimemsg)
                return

            meal_date = str(meal_date.content) # 171121
            meal_date = '20' + meal_date[:2] + '.' + meal_date[2:4] + '.' + meal_date[4:6] # 2017.11.21

            s = meal_date.replace('.', ', ') # 2017, 11, 21

            #한자리수 달인 경우를 해결하기위함
            if int(s[6:8]) < 10:
                s = s.replace(s[6:8], s[7:8])

            ss = "datetime.datetime(" + s + ").weekday()"
            try:
                whatday = eval(ss)
            except:
                warnning = discord.Embed(title="Plz Retry", description='올바른 값으로 다시 시도하세요 : !식단', color=0xff0000)
                await message.channel.send(message.channel, embed=warnning)
                return

            await print_get_meal(meal_date, whatday, message)

    client.run(TOKEN)

    #대기 시간 초과로 봇이 종료되었을 때 자동으로 재실행을 위함
    #import sys, os
    executable = sys.executable
    args = sys.argv[:]
    args.insert(0, sys.executable)
    print("Respawning")
    os.execvp(executable, args)

if __name__ == '__main__':
    main()
