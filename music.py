from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pyautogui import press
from pynput import keyboard
from threading import Thread
import re
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
from mutagen import File
import os

driverPath = '/path/to/chromedriver'
downloadFolderPath = '/path/to/Downloads/folder/'

title, main_artist, other_artists = '', '', ''
title_search, main_artist_search = '', ''
command_exit, command_next, command_back, command_download, command_search = False, False, False, False, False
exit_loop = False
song_number = 3
items1 = 'Ą', 'ą', 'Ć', 'ć', 'Ę', 'ę', 'Ł', 'ł', 'Ń', 'ń', 'Ó', 'ó', 'Ś', 'ś', 'Ź', 'ź', 'Ż', 'ż'
items2 = '%A1', '%B1', '%C6', '%E6', '%CA', '%EA', '%A3', '%B3', '%D1', '%F1', '%D3', '%F3', '%A6', '%B6', '%AC', \
         '%BC', '%AF', '%BF'
items3 = 'Ą', 'ą', 'Ć', 'ć', 'Ę', 'ę', 'Ł', 'ł', 'Ń', 'ń', 'Ó', 'ó', 'Ś', 'ś', 'Ź', 'ź', 'Ż', 'ż', '(', ')',\
                 "'", ',', 'ä', 'ë'

driver = webdriver.Chrome(driverPath)
driver.close()


def song_data():
    global title, main_artist, other_artists
    print('')
    print('TITLE:')
    title = '-> '
    title = (input(title)).title()
    print('MAIN ARTIST:')
    main_artist = '-> '
    main_artist = (input(main_artist)).title()
    print('OTHER ARTISTS:')
    other_artists = '-> '
    other_artists = (input(other_artists)).title()
    if other_artists == '':
        other_artists = None


def change_for_search():
    global title, main_artist, title_search, main_artist_search
    title_search = title
    for counter in range(0, 18):
        title_search = title_search.replace(items1[counter], items2[counter])
    main_artist_search = main_artist
    for counter in range(0, 18):
        main_artist_search = main_artist_search.replace(items1[counter], items2[counter])


def open_website():
    global driver
    driver = webdriver.Chrome(driverPath)
    driver.set_window_rect(1000, 0, 1000, 1100)
    driver.get('http://muzyka.teledyski.info/index.html?text=' + main_artist_search + ' - ' + title_search +
               '&strona=0&file=global_test&name=eplik&dalej=Szukaj')
    while True:
        find_accept_button = driver.page_source
        find_accept_button = BeautifulSoup(find_accept_button, 'html.parser')
        find_accept_button = find_accept_button.find('button', {'class': 'button_button--sYDKO details_save--3nDG7'})
        if find_accept_button is not None:
            find_accept_button = find_accept_button.text
            if find_accept_button == 'Zaakceptuj wszystko':
                try:
                    driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div[2]/button[2]').click()
                    break
                except(ValueError, Exception):
                    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div/div[2]/button[2]').click()
                    break
        sleep(0.5)


def open_first_song():
    global driver
    driver.find_element_by_xpath('/html/body/center/div[3]/div/table[2]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/'
                                 'tr/td/table/tbody/tr/td/table[2]/tbody/tr[3]/td[2]/a').click()
    driver.switch_to.window(driver.window_handles[1])
    while True:
        find_accept_button = driver.page_source
        find_accept_button = BeautifulSoup(find_accept_button, 'html.parser')
        find_accept_button = find_accept_button.find('button', {'class': 'button_button--sYDKO details_save--3nDG7'})
        if find_accept_button is not None:
            find_accept_button = find_accept_button.text
            if find_accept_button == 'Zaakceptuj wszystko':
                try:
                    driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div[2]/button[2]').click()
                except(ValueError, Exception):
                    try:
                        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div/div[2]/button[2]').click()
                    except(ValueError, Exception):
                        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/button[2]').click()
                break
        sleep(0.5)
    driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]').click()
    press('tab')
    press('space')
    in_song_listener()


def open_next_song():
    global driver, song_number
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    while True:
        try:
            driver.find_element_by_xpath('/html/body/center/div[3]/div/table[2]/tbody/tr[1]/td/table/tbody/tr/td/'
                                         'table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[' + str(song_number) +
                                         ']/td[2]/a').click()
            break
        except(ValueError, Exception):
            try:
                press('down')
                driver.find_element_by_xpath('/html/body/center/div[3]/div/table[2]/tbody/tr[1]/td/table/tbody/tr/td/'
                                             'table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr['
                                             + str(song_number) + ']/td[2]/a').click()
                break
            except(ValueError, Exception):
                song_number += 1
    driver.switch_to.window(driver.window_handles[1])
    while True:
        find_comments = driver.page_source
        find_comments = BeautifulSoup(find_comments, 'html.parser')
        find_comments = find_comments.find('div', {'class': 'heading-block'})
        if find_comments is not None:
            find_comments = find_comments.text
            if find_comments == '\nKomentarze\n':
                break
        sleep(0.5)
    driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]').click()
    press('tab')
    press('space')
    in_song_listener()


def open_previous_song():
    global driver, song_number
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    while True:
        try:
            driver.find_element_by_xpath('/html/body/center/div[3]/div/table[2]/tbody/tr[1]/td/table/tbody/tr/td/'
                                         'table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[' + str(song_number) +
                                         ']/td[2]/a').click()
            break
        except(ValueError, Exception):
            try:
                press('up')
                driver.find_element_by_xpath('/html/body/center/div[3]/div/table[2]/tbody/tr[1]/td/table/tbody/tr/td/'
                                             'table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr['
                                             + str(song_number) + ']/td[2]/a').click()
                break
            except(ValueError, Exception):
                song_number -= 1
    driver.switch_to.window(driver.window_handles[1])
    while True:
        find_comments = driver.page_source
        find_comments = BeautifulSoup(find_comments, 'html.parser')
        find_comments = find_comments.find('div', {'class': 'heading-block'})
        if find_comments is not None:
            find_comments = find_comments.text
            if find_comments == '\nKomentarze\n':
                break
        sleep(0.5)
    driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]').click()
    press('tab')
    press('space')
    in_song_listener()


def search():
    global command_exit, exit_loop
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    find_songs = driver.page_source
    while exit_loop is False:
        def on_press(key):
            global exit_loop, command_exit
            if str(key) == 'Key.esc':
                exit_loop = True
                command_exit = True

        with keyboard.Listener(on_press=on_press) as listener:
            def time_out(period_sec: int):
                sleep(2)
                listener.stop()
                return period_sec

            Thread(target=time_out, args=(5.0,)).start()
            listener.join()
            try:
                driver.switch_to.window(driver.window_handles[1])
                exit_loop = True
            except(ValueError, Exception):
                pass
    if command_exit is True:
        command_exit = False
        exit_driver()
    else:
        exit_loop = False
        while True:
            find_comments = driver.page_source
            find_comments = BeautifulSoup(find_comments, 'html.parser')
            find_comments = find_comments.find('div', {'class': 'heading-block'})
            if find_comments is not None:
                find_comments = find_comments.text
                if find_comments == '\nKomentarze\n':
                    break
            sleep(0.5)
        find_song_name = driver.page_source
        find_song_name = BeautifulSoup(find_song_name, 'html.parser')
        find_song_name = find_song_name.find('h1', {'class': 'masthead-subtitle'})
        find_song_name = find_song_name.text
        find_song_name = re.findall('Pobieranie pliku +(.*).', find_song_name)
        find_song_name = find_song_name[0]
        find_song_name = find_song_name.strip()
        find_songs = BeautifulSoup(find_songs, 'html.parser')
        find_songs = find_songs.find_all('a', {'target': '_blank'})
        counter = 0
        while counter < 30:
            try:
                find_songs[counter] = find_songs[counter].text
                counter += 1
            except (ValueError, Exception):
                counter += 1
        for counter in range(0, len(find_songs)):
            if find_songs[counter] == find_song_name:
                global song_number
                song_number = counter - 2
        driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]').click()
        press('tab')
        press('space')
        in_song_listener()


def in_song_listener():
    global command_exit, command_next, command_back, command_download, command_search, song_number

    def on_press(key):
        global command_exit, command_next, command_back, command_download, command_search
        if str(key) == 'Key.esc':
            command_exit = True
            return False
        try:
            key = eval(str(key))
            if str(key) == ']':
                command_next = True
                return False
            if str(key) == '[':
                command_back = True
                return False
            if str(key) == 'd':
                command_download = True
                return False
            if str(key) == 's':
                command_search = True
                return False
        except(ValueError, Exception):
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    if command_exit is True:
        command_exit = False
        exit_driver()
    if command_next is True:
        command_next = False
        song_number += 1
        open_next_song()
    if command_back is True:
        command_back = False
        if song_number > 3:
            song_number -= 1
        open_previous_song()
    if command_download is True:
        command_download = False
        download()
    if command_search is True:
        command_search = False
        search()


def download():
    global driver
    find_title = driver.page_source
    find_title = BeautifulSoup(find_title, 'html.parser')
    find_title = find_title.find('h1', {'class': 'masthead-subtitle'})
    find_title = find_title.text
    find_title = ' '.join(find_title.splitlines())
    find_title = re.findall('Pobieranie pliku +(.*).mp3', find_title)
    find_title = find_title[0]
    driver.find_element_by_xpath('//*[@id="pobierz"]').click()
    for counter in range(0, len(items3)):
        find_title = find_title.replace(items3[counter], '_')
    while not os.path.exists(downloadFolderPath + find_title + '.mp3'):
        sleep(0.5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    try:
        file = ID3(downloadFolderPath + find_title + '.mp3')
        file.delall("APIC")
        file.save()
    except(ValueError, Exception):
        file = File(downloadFolderPath + find_title + '.mp3')
        file.add_tags()
        file.save()
    audio = EasyID3(downloadFolderPath + find_title + '.mp3')
    audio['title'] = title
    audio['artist'] = main_artist
    audio.save()
    if other_artists is None:
        os.rename(downloadFolderPath + find_title + '.mp3',
                  downloadFolderPath + title + ' - ' + main_artist + '.mp3')
    else:
        os.rename(downloadFolderPath + find_title + '.mp3',
                  downloadFolderPath + title + ' - ' + main_artist + ' ft. ' + other_artists + '.mp3')
    exit_program()
    get_song()


def exit_driver():
    driver.close()
    try:
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
    except(ValueError, Exception):
        pass
    exit_program()
    get_song()


def exit_program():
    print('')
    print('EXIT PROGRAM?(y)')
    close_program = '-> '
    close_program = input(close_program)
    if close_program == 'y':
        exit()


def get_song():
    song_data()
    change_for_search()
    open_website()
    open_first_song()


get_song()
