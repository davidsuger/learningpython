import os
import pathlib

mp3Names = ['3 - At home and in the garden',
            '5 - In the living room',
            '6 - In the kitchen',
            '7 - In town',
            '8 - Getting around',
            '9 - At school',
            '10 - Sports and hobbies',
            '11 - Family and special occasions',
            '12 - Jobs',
            '13 - My body and health',
            '14 - Clothes',
            '15 - At the market',
            '16 - At the café',
            '17 - On the farm',
            '18 - At the zoo',
            '19 - Weather and seasons',
            '20 - Numbers and days',
            '21 - Around the world',
            '22 - Where are they',
            '23 - Story words',
            '24 - Colours and shapes',
            '25 - What are they like',
            '26 - Opposite words',
            '27 - I can…',
            '28 - I like to…']

p = pathlib.Path('C:/Users/IBM_ADMIN/Desktop/English')
counter = 0
for x in p.iterdir():
    if x.is_dir():
        print(x)
        newfile = open('C:/Users/IBM_ADMIN/Desktop/English/' + mp3Names[counter] + '.mp3',
                       'wb')
        sectionPath = pathlib.Path(x)
        for y in sectionPath.iterdir():
            print(y)
            print(y.name)
            print('{:0>4}'.format(y.name))
            target = str(x) + '/' + '{:0>4}'.format(y.name)
            p = pathlib.Path(y)
            p.rename(target)
            print(target)
            mp3 = open(target, 'rb')
            newfile.write(mp3.read())
            mp3.close()
        newfile.close()
        counter = counter + 1
#
# newfile = open('C:/Users/IBM_ADMIN/Desktop/3 - At home and in the garden/3 - At home and in the garden.mp3', 'wb')
#
# for i in range(1, 61):
#     print(i)
#     print('C:/Users/IBM_ADMIN/Desktop/3 - At home and in the garden/' + str(i))
#     mp3 = open('C:/Users/IBM_ADMIN/Desktop/3 - At home and in the garden/' + str(i), 'rb')
#     newfile.write(mp3.read())
#     mp3.close()
#
# newfile.close()
