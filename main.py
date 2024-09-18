import flet as ft
import os
from time import sleep
from random import choice, randint
from math import sqrt

if not os.path.exists('settings.txt'):
    with open('settings.txt', 'w') as file:
        file.write('30;10;2,1,100;2,1,100;2,1,100;50;100')

with open('settings.txt', 'r') as file:
    sets = file.read().split(';')
print(sets)

standarts = ['30', '10' ,['2', '1', '100'],['2', '1', '100'], ['2', '1', '100'], '50' , '100']

def main(page: ft.Page):
    def random_exp(what):
        expression = []
        if what == 'a':
            shs = sets[2].split(',')
            for i in range(int(shs[0])):
                expression.append(f'{randint(int(shs[1]), int(shs[2]))}')
            expression = '+'.join(expression)
            answer = eval(expression)
            return [expression, answer]
        elif what == 's':
            shs = sets[3].split(',')
            for i in range(int(shs[0])):
                expression.append(f'{randint(int(shs[1]), int(shs[2]))}')
            expression = '-'.join(expression)
            answer = eval(expression)
            return [expression, answer]
        elif what == 'm':
            shs = sets[4].split(',')
            for i in range(int(shs[0])):
                expression.append(f'{randint(int(shs[1]), int(shs[2]))}')
            answer = eval('×'.join(expression))
            return ['×'.join(expression), answer]
        elif what == 'sqr':
            shs = int(sets[5])
            expression = randint(1, shs)
            answer = expression ** 2
            return [str(expression) + '^2', answer]
        elif what == 'sqrt':
            shs = int(sets[6])
            expression = randint(1, int(sqrt(shs))) ** 2
            answer = sqrt(expression)
            return [str(expression), answer]


    def menu(e):
        if e.control.selected_index:
            right.content = settings
        else:
            right.content = game
            if all([i == '0' for i in sets[2:6]]):
                exp.value = 'You chose nothing in settings'
                play_btn.disabled = True
            else:
                exp.value = 'Start the game'
                play_btn.disabled = False
        page.update()
    def start(e):
        if e.control.icon == ft.icons.PLAY_ARROW_ROUNDED:
            if exp.value == 'The End':
                stat.rows.clear()
            exp.value = "Okay, let's go"
            count_left.visible = True
            count_left.value = 'left: ' + sets[1]
            e.control.icon = ft.icons.PAUSE
            n = 2
            available = ['a','s','m','sqr','sqrt']
            available = [name for index, name in enumerate(available,start=2) if sets[index] != '0']
            expression = random_exp(choice(available))
            print(expression)
            count = 0
            for i in range(int(sets[0])*2*int(sets[1]) + 6):
                if n > int(sets[0]) or ans.value == str(expression[1]):
                    n = 0
                    count += 1
                    count_left.value = 'left: ' + str(int(sets[1]) - count)
                    stat.rows.append(ft.DataRow([ft.DataCell(ft.Text(str(count))),
                                                ft.DataCell(ft.Text(expression[0])),
                                                ft.DataCell(ft.Text(ans.value)),
                                                ft.DataCell(ft.Text(str(expression[1])))]))
                    ans.value = ''
                    expression = random_exp(choice(available))
                    exp.value = expression[0]
                    if count == int(sets[1]):
                        exp.value = 'The End'
                        play_btn.icon = ft.icons.PLAY_ARROW_ROUNDED
                        page.update()
                        break
                    page.update()
                if i == 6:
                    exp.value = expression[0]
                if i % 2 == 0:
                    if i <= 3:
                        time.value = '0:0' + str(n)
                        n -= 1
                    else:
                        if n >= 10:
                            time.value = '0:' + str(n)
                        else:
                            time.value = '0:0' + str(n)
                        n += 1
                    page.update()

                sleep(0.5)

        else:
            e.control.icon = ft.icons.PLAY_ARROW_ROUNDED
        page.update()
    def expandList(e):
        name = names[e.control.parent.controls[1].value]
        if name.controls[1].visible:
            name.controls[1].visible = False
        else:
            name.controls[1].visible = True
        name.update()
    def save(e):
        string = ''
        for index, i in enumerate(settings.controls[:-1]):
            values = i.controls[1]
            try:
                if index == 0:
                    if values.value and int(values.value) > 0:
                        string += values.value +';'
                    else:
                        string += standarts[0] + ';'
                elif index == 1:
                    if values.value and int(values.value) > 0:
                        string += values.value +';'
                    else:
                        string += standarts[1] + ';'
                elif index == 2 or index == 3 or index == 4:
                    if not i.controls[0].controls[0].value:
                        string += '0;'
                    else:
                        numbers = values.controls
                        if numbers[0].controls[1].value != '':
                            if int(numbers[0].controls[1].value) >= 2:
                                string += numbers[0].controls[1].value +','
                        else:
                            string += standarts[index][0] + ','
                        if numbers[1].controls[1].value != '' and numbers[1].controls[3].value != '':
                            if int(numbers[1].controls[1].value) > 0 and int(numbers[1].controls[3].value) > int(numbers[1].controls[1].value):
                                string +=  numbers[1].controls[1].value +','+ numbers[1].controls[3].value+';'
                                continue
                        string += standarts[index][1] + ',' + standarts[index][2] + ';'
                elif index == 5 or index == 6:
                    if not i.controls[0].controls[0].value:
                        string += '0;'
                    else:

                        if values.controls[1].value != '':
                            if int(values.controls[1].value) > 0:
                                string += values.controls[1].value + ';'
                                continue
                        string += standarts[index] + ',' + standarts[index] + ';'

            except ValueError:
                if len(settings.controls) == 8:
                    settings.controls.append(ft.Text('There are invalid values',size=15,color='red'))
                    settings.update()
                break
        for index, i in enumerate(string.split(';')[:-1]):
            if sets[index] != i:
                sets[index] = i
        with open('settings.txt', 'w') as file:
            file.write(';'.join(sets))


    left = ft.NavigationRail(min_width=100,
                             min_extended_width=400,
                            destinations=[ft.NavigationRailDestination(icon=ft.icons.GAMEPAD, label='Game'),
                                          ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label='Settings')],
                            on_change=menu)

    timea = ft.Row([ft.Text('Time for answer'), ft.TextField(value=sets[0],width=50,height=50),ft.Text('sec')])

    count_exp = ft.Row([ft.Text('The count of examples'),ft.TextField(value=sets[1],width=50,height=50)])

    ams = ft.Column(controls=[ft.Row(controls=[ft.Text('       Number of terms'),ft.TextField(width=50,height=50)]),
                            ft.Row([ft.Text('       min'),
                                    ft.TextField(width=50, height=50),
                                    ft.Text('max'),
                                    ft.TextField(width=50, height=50)])],
                    visible=False)


    a = ft.Column(controls=[ft.Row(controls=[ft.Checkbox(),ft.Text('Amount', size=21),ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_DOWN, on_click=expandList)]), ams])

    ss = ft.Column([ft.Row([ft.Text('       Number of subtrahends'),ft.TextField(width=50,height=50)]),
                    ft.Row([ft.Text('       min'),
                            ft.TextField(width=50, height=50),
                            ft.Text('max'),
                            ft.TextField(width=50, height=50)])],
                    visible=False)

    s = ft.Column(controls=[ft.Row(controls=[ft.Checkbox(),ft.Text('Subtraction', size=21),ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_DOWN, on_click=expandList)]), ss])

    ms = ft.Column([ft.Row([ft.Text('       Number of multiplicands'),ft.TextField(width=50,height=50)]),
                    ft.Row([ft.Text('       min'),
                            ft.TextField(width=50, height=50),
                            ft.Text('max'),
                            ft.TextField(width=50, height=50)])],
                    visible = False)
    m = ft.Column(controls=[ft.Row(controls=[ft.Checkbox(),ft.Text('Multiplication', size=21),ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_DOWN, on_click=expandList)]), ms])

    sqr = ft.Column(controls=[ft.Row(controls=[ft.Checkbox(),ft.Text('Square', size=21),ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_DOWN, on_click=expandList)]),
                             ft.Row([ft.Text('       up to'),ft.TextField(width=50, height=50)],
                    visible=False)])

    sqrt = ft.Column(controls=[ft.Row(controls=[ft.Checkbox(), ft.Text('Sqrt', size=21), ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_DOWN, on_click=expandList)]),
                               ft.Row([ft.Text('       up to'),ft.TextField(width=50, height=50)],
                      visible=False)])
    indexes = {2: a, 3: s, 4: m, 5: sqr, 6: sqrt}
    for index, i in enumerate(sets[2:],start=2):
        if sets[index] != '0':
            indexes[index].controls[0].controls[0].value = True
            if index <= 4:
                indexes[index].controls[1].controls[0].controls[1].value = i.split(',')[0]
                indexes[index].controls[1].controls[1].controls[1].value = i.split(',')[1]
                indexes[index].controls[1].controls[1].controls[3].value = i.split(',')[2]
            elif index > 4:
                indexes[index].controls[1].controls[1].value = i
        else:
            indexes[index].controls[0].controls[0].value = False

    save = ft.TextButton('Save', on_click=save, style=ft.ButtonStyle(bgcolor='blue',color='white',padding=15))
    play_btn = ft.IconButton(icon=ft.icons.PLAY_ARROW_ROUNDED,icon_size=35, icon_color='blue', on_click=start)
    exp = ft.Text('Start the game',size=32,color='black')
    if all([i == '0' for i in sets[2:6]]):
        play_btn.disables = True
        exp.value = 'You chose nothing in settings'
    time = ft.Text('0:03',size=30,weight='bold',color='blue')
    count_left = ft.Text('left: ',size=30, color='blue', visible=False)
    ans = ft.TextField(height=50, width=200)
    stat = ft.DataTable(
                        columns=[
                                ft.DataColumn(ft.Text('Attempt')),
                                ft.DataColumn(ft.Text('Expression')),
                                ft.DataColumn(ft.Text('Your answer')),
                                ft.DataColumn(ft.Text('Right answer'))
                        ]
    )
    game = ft.Column([ft.Row([time,count_left, play_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        exp, ans, stat],horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    settings = ft.Column(controls=[timea, count_exp, a, s, m, sqr, sqrt, save],scroll=ft.ScrollMode.ALWAYS)
    right = ft.Container(content=game, expand=True)

    page.add(ft.Row([left, right],expand=True))

    names = {"Amount": a,
            "Subtraction":s,
            "Multiplication": m,
            "Square": sqr,
            "Sqrt": sqrt}


ft.app(target=main)
