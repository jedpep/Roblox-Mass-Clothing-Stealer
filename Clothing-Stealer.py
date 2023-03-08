import requests
import os
import ctypes
import time
import sys
os.system('cls')
ctypes.windll.kernel32.SetConsoleTitleW("Clothing stealer | skittles#9999")

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

if not os.path.isdir('files'):
    print('Looks like this is your first time using this clothing stealer\nWould you like to start the installation?')
    if input('\n(y/n) :') == 'y':
        if not os.path.isdir('files'):
            os.mkdir('files')
            with open('files/remove.exe', 'wb') as f:
                print('Installing "remove.exe"')
                f.write(requests.get('https://github.com/jedpep/Roblox-Mass-Clothing-Stealer/blob/main/remove.exe?raw=true').content)
        print('Installation finished')
        input('Press RETURN to finish...')
        exit()
    else:
        exit()

def main(ID, MODE, WATERMARK):
    global counter
    counter = 0
    IDs = []
    def download(clothingID, assetType):
        if not os.path.isdir('output'):
            os.mkdir('output')

        def a2n(a): 
            if str(a) == '11': return '-Shirt'
            if str(a) == '12': return '-Pants'
            if str(a) == 'idk': return ('')

        def getpng():
            global counter
            counter = counter + 1
            print(f'Downloading clothing ID: {clothingID} | {counter}/{len(IDs)}')
            assetdelivery = requests.get(f'https://assetdelivery.roblox.com/v1/assetId/{clothingID}').json()['location']
            assetid = str(requests.get(assetdelivery).content).split('<url>http://www.roblox.com/asset/?id=')[1].split('</url>')[0]
            png = requests.get(f'https://assetdelivery.roblox.com/v1/assetId/{assetid}').json()['location']
            return requests.get(png).content
        
        Image = getpng()

        with open(f'output/{clothingID}{a2n(assetType)}.png', 'wb') as f:
            f.write(Image)
        if WATERMARK == 'y':
            #print(f'{os.getcwd()}/files/remove.exe {os.getcwd()}/output/{clothingID}.png')
            os.system(f'{os.getcwd()}/files/remove.exe {os.getcwd()}/output/{clothingID}{a2n(assetType)}.png')
    
    if MODE == 'group':
        def getClothingFromGroup(groupID):
            print('Scraping all catalog items from group')
            cursor = ''
            while 1:
                ratelimited = False
                catalog = requests.get(f'https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=2&IncludeNotForSale=false&Limit=30&CreatorTargetId={groupID}&cursor={cursor}').json()
                if not 'nextPageCursor' in catalog:
                    print('Ratelimited, waiting 30 seconds...')
                    ratelimited = True
                    time.sleep(30)
                    pass
                if ratelimited == False:
                    print(f"Cursor {catalog['nextPageCursor']}")
                    cursor = catalog['nextPageCursor']
                    for x in catalog['data']:
                        if str(x['assetType']) == '11' or str(x['assetType']) == '12':
                            IDs.append([x['id'], x['assetType']])
                if not cursor: break

            return IDs
        
        catalog = getClothingFromGroup(ID)
        print('Done scraping...\nDownloading all catalog items')
        for x in catalog:
            download(x[0], x[1])
        print('Done downloading all items')
    else:
        download(ID, 'idk') # i hate the roblox api

    input('Finished downloading assets!\nPress RETURN to exit...')

print(r"""
        _________ .__          __  .__    .__                   _________ __                .__                
        \_   ___ \|  |   _____/  |_|  |__ |__| ____    ____    /   _____//  |_  ____ _____  |  |   ___________ 
        /    \  \/|  |  /  _ \   __\  |  \|  |/    \  / ___\   \_____  \\   __\/ __ \\__  \ |  | _/ __ \_  __ \
        \     \___|  |_(  <_> )  | |   Y  \  |   |  \/ /_/  >  /        \|  | \  ___/ / __ \|  |_\  ___/|  | \/
        \______  /____/\____/|__| |___|  /__|___|  /\___  /  /_______  /|__|  \___  >____  /____/\___  >__|   
                \/                      \/        \//_____/           \/           \/     \/          \/         
""")

mode = input('Group or clothing: ').lower()
if mode != 'group' and mode != 'clothing': exit()
id = input(f'{mode} ID: ')
wm = input('Remove water marks? (y/n) : ')
print('\n\n')
main(id, mode, wm)