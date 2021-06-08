import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from collections import defaultdict


# Функция получения текста html-страницы
def get_html(url):
    r = requests.get(url)
    return r.text


# Функция получения всех событий для marathon.bet на баскетбол
def get_all_event_marathonbet(html):
    all_players = []
    all_K = []
    soup = BeautifulSoup(html, 'lxml')
    all_event = soup.find('div', class_ = "sport-category-content").find_all('div', class_='bg coupon-row')
    for players in all_event:
        if '- ' in players['data-event-name']:
            players = players['data-event-name'].replace('- ', '+').split('+')
        elif '@ ' in players['data-event-name']:
            players = players['data-event-name'].replace('@ ', '+').split('+')
        #print(players)
        player_1 = players[0].strip()
        player_2 = players[1].strip()
        all_players.append(player_1)
        all_players.append(player_2)

    for g in all_event:
        if g.find('td',colspan="1").find('span',class_="selection-link active-selection") == None:
            K1 = 1
            K2 = 1
            all_K.append(K1)
            all_K.append(K2)
            continue
        K1 = g.find('td',colspan="1").find('span',class_="selection-link active-selection").text
        K2 = g.find('td', colspan="1").find('span', class_="selection-link active-selection").findNext('span').text
        all_K.append(K1)
        all_K.append(K2)
    #print(all_players)
    return all_players, all_K


# Функция получения всех событий для tennisi на баскетбол
def get_all_event_tennisi(html):
    all_players = []
    all_K = []
    new_all_event = []
    soup = BeautifulSoup(html, 'lxml')
    #all_tables = soup.findAll('table')#('td', align = "left", class_ = "WO", bgcolor = "#FFDECF")#('a', target='main')
    all_event = soup.findAll('tr', align = "center", bgcolor = "#FFF2C5")
    '''for table in all_tables:
        event = table.findAll('td', align = "left", class_ = "WO", bgcolor = "#FFDECF")
        all_event.extend(event)'''

    for event in all_event:
        players = event.find('td', align = "left", class_ = "WO", bgcolor = "#FFDECF").find('a', target='main').get_text()
        #all_event.index[players] = players
        #print(players)
        if '(' in players or ' - ' not in players or 'Спец' in players:
            #all_event.remove[all_event.index(event)]
            continue
        new_all_event.append(event)
        players = players.replace('- ', '+').split('+')
        player_1 = players[0].strip()
        player_2 = players[1].strip()
        #print(player_1,': ',player_2)
        all_players.append(player_1)
        all_players.append(player_2)
        #print(all_players)

    #print(len(all_players))

    for g in new_all_event:
        if g.find('a', onclick = "return b(this,0);", id="p") == None:
            continue
        K1 = g.find('a', onclick = "return b(this,0);", id="p").get_text()
        K2 = g.find('a', onclick = "return b(this,0);", id="p").findNext('a').get_text()
        if '+' in K2 or '-' in K2 or '+' in K1 or '-' in K1:
            K1 = 1
            K2 = 1
        '''if g.find('td', align = "center", class_ = "WO").get_text() == "&nbsp;&nbsp;":
           K1 = 1
           K2 = g.find('a', onclick = "return b(this,0);", id="p").get_text()
           if '+' in K2 or '-' in K2:
                K2 = 1
        else:
            K1 = g.find('a', onclick = "return b(this,0);", id="p").get_text()
            K2 = g.find('a', onclick = "return b(this,0);", id="p").findNext('a').get_text()
            if '+' in K2 or '-' in K2:
                K2 = 1
        K1 = g.find('a', onclick = "return b(this,0);", id="p").get_text() #.find('td', align = "center", class_ = "WO")
        K2 = g.find('a', onclick = "return b(this,0);", id="p").findNext('a').get_text()
        if '+' in K2 or '-' in K2:
                K2 = 1
                K1 = 1
        if g.find('td', align = "center", class_ = "WO").get_text() == "&nbsp;&nbsp;":#.find('a', onclick = "return b(this,0);", id="p") == None:
            K1 = 1
            K2 = g.find('a', onclick = "return b(this,0);", id="p").findNext('a').get_text()
        else:
            K1 = g.find('a', onclick = "return b(this,0);", id="p").get_text() #.find('td', align = "center", class_ = "WO")
            K2 = g.find('a', onclick = "return b(this,0);", id="p").findNext('a').get_text()
            if '+' in K2 or '-' in K2:
                K2 = 1
                K1 = 1
            if g.find('td', align = "center", class_ = "WO").findNext('td').get_text() == "&nbsp;&nbsp;":
                K2 = 1
            else:
                K2 = g.find('a', onclick = "return b(this,0);", id="p").findNext('a').get_text()'''
        #if '+' in K2 or '-' in K2:
            #if g.find('td', align = "center", class_ = "WO").find('a', onclick = "return b(this,0);", id="p").get_text()
        #print(K1, K2)
        all_K.append(K1)
        all_K.append(K2)
    
    #print(len(all_K))

    '''for z in all_players:
        i = all_players.index(z)
        if i % 2 == 0:
            print(all_players[i], 'V ', all_players[i+1], ' ', all_K[i], ' ', all_K[i+1])'''

    return all_players, all_K

# Функция формирования из списка игроков пар, т.е. самих матчей
def create_arr_couple(arr_players):
    arr_couple = []
    for i in range(0, len(arr_players), 2):
        arr_couple.append(arr_players[i] + ' V ' + arr_players[i + 1])
    return arr_couple

# Функция формирования словаря вида {'*имя игрока* V *имя игрока*':['кф', 'кф']}
def create_dict(arr_couple, arr_key):
    cat = defaultdict(list)
    scet = 0
    try:
        for i in range(len(arr_couple)):
            cat[arr_couple[i]].append(arr_key[scet])
            cat[arr_couple[i]].append(arr_key[scet + 1])
            scet += 2
        return dict(cat)
    except IndexError:
        print('Количество игроков не совпадает с количеством кэфов')


# Функция нахождения одинаковых событий
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Функция нахождения вилки
def find_vilka(K1, K2):
    return 1/float(K1)+1/float(K2)

# функция подсчета того, сколько составит чистый выигрыш
def profit(K, summa_max,summa_min):
    print("Выигрыш составит: "+str((float(K)*summa_max)-summa_min-summa_max))

# Функция расчета, сколько и на какой коэффициент нужно ставить
def raschet_vilki(K1,K2,summa_max = 100):

    if K1<K2:
        summa_min = (float(K1)*summa_max)/float(K2)
        print('На коэффициент {}'.format(K1)+' ставим {} '.format(summa_max))
        print('На коэффициент {}'.format(K2) + ' ставим {} '.format(summa_min))
        profit(K1, summa_max, summa_min)

    else:
        summa_min = (float(K2) * summa_max) / float(K1)
        print('На коэффициент {}'.format(K1) + ' ставим {} '.format(summa_min))
        print('На коэффициент {}'.format(K2) + ' ставим {} '.format(summa_max))
        profit(K2, summa_max, summa_min)


# Функция нахождения общих матчей двух контор
def find_general(a_couple, b_couple, dict_a, dict_b):
    for elem_a in a_couple:
        for elem_b in b_couple:
            d = similar(elem_a, elem_b)
            if d > 0.75:

                arr_K_a = dict_a[elem_a]
                arr_K_b = dict_b[elem_b]
                Ko_1 = find_vilka(arr_K_a[0], arr_K_b[1])
                Ko_2 = find_vilka(arr_K_a[1], arr_K_b[0])
                '''print(elem_a)
                print(elem_b)
                print("Ko_1: " + str(Ko_1))
                print("Ko_2: " + str(Ko_2))'''

                if Ko_1<1:
                    print(elem_a)
                    print(elem_b)
                    print("Ko_1: " + str(Ko_1))
                    print("Ko_2: " + str(Ko_2))
                    raschet_vilki(arr_K_a[0], arr_K_b[1])

                if Ko_2<1:
                    print(elem_a)
                    print(elem_b)
                    print("Ko_1: " + str(Ko_1))
                    print("Ko_2: " + str(Ko_2))
                    raschet_vilki(arr_K_a[1], arr_K_b[0])


# Основная функция
def main():
    url_marathonbet = 'https://www.marathonbet.ru/su/betting/Basketball+-+6?interval=ALL_TIME'
    html_marathonbet = get_html(url_marathonbet)
    all_players_marathonbet, all_K_marathonbet = get_all_event_marathonbet(html_marathonbet)
    arr_couple_marathonbet = create_arr_couple(all_players_marathonbet)
    marathonbet_dict = create_dict(arr_couple_marathonbet, all_K_marathonbet)

    url_tennisi = 'https://tennisi.bet/rt/cgi/!rt_home.CategoryInfo?mcmd=5&gameid=5&categoryid=140&lang=rus&more=today&lang=rus'
    html_tennisi = get_html(url_tennisi)
    all_players_tennisi, all_K_tennisi = get_all_event_tennisi(html_tennisi)
    arr_couple_tennisi = create_arr_couple(all_players_tennisi)
    tennisi_dict = create_dict(arr_couple_tennisi, all_K_tennisi)

    find_general(arr_couple_marathonbet, arr_couple_tennisi , marathonbet_dict, tennisi_dict)



if __name__ == '__main__':
    main()