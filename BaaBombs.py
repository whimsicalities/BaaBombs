from tkinter import Tk, Canvas, PhotoImage, Button, Entry
import os


class cSheep:
    def __init__(self, x, y, direction, alive):
        self.direction = direction
        self.up_image = PhotoImage(file='sheep_up.png')
        self.down_image = PhotoImage(file='sheep_down.png')
        self.left_image = PhotoImage(file='sheep_left.png')
        self.right_image = PhotoImage(file='sheep_right.png')
        if direction == 3:
            self.icon = canvas.create_image(x, y, anchor='nw',
                                            image=self.left_image)
        elif direction == 1:
            self.icon = canvas.create_image(x, y, anchor='nw',
                                            image=self.right_image)
        elif direction == 2:
            self.icon = canvas.create_image(x, y, anchor='nw',
                                            image=self.down_image)
        else:
            self.icon = canvas.create_image(x, y, anchor='nw',
                                            image=self.up_image)
        self.max_dir_timeout = 1
        self.direction_timeout = 0
        self.alive = True

    def reverse_dir(self):
        if self.direction == 0:
            self.direction = 2
            canvas.itemconfig(self.icon, image=self.down_image)
        elif self.direction == 1:
            self.direction = 3
            canvas.itemconfig(self.icon, image=self.left_image)
        elif self.direction == 2:
            self.direction = 0
            canvas.itemconfig(self.icon, image=self.up_image)
        elif self.direction == 3:
            self.direction = 1
            canvas.itemconfig(self.icon, image=self.right_image)
        self.move()
        self.direction_timeout = self.max_dir_timeout

    def decrement_reversedir_timeout(self):
        self.direction_timeout = self.direction_timeout - 1

    def reset_dir(self):
        self.direction = -1

    def go_north(self, event):
        if self.direction_timeout <= 0:
            canvas.itemconfig(self.icon, image=self.up_image)
            self.direction = 0
            self.direction_timeout = self.max_dir_timeout

    def go_east(self, event):
        if self.direction_timeout <= 0:
            self.direction = 1
            canvas.itemconfig(self.icon, image=self.right_image)
            self.direction_timeout = self.max_dir_timeout

    def go_south(self, event):
        if self.direction_timeout <= 0:
            self.direction = 2
            canvas.itemconfig(self.icon, image=self.down_image)
            self.direction_timeout = self.max_dir_timeout

    def go_west(self, event):
        if self.direction_timeout <= 0:
            self.direction = 3
            canvas.itemconfig(self.icon, image=self.left_image)
            self.direction_timeout = self.max_dir_timeout

    def move(self):
        if self.direction == 0:
            canvas.move(self.icon, 0, -2)
            canvas.pack()
        elif self.direction == 1:
            canvas.move(self.icon, 2, 0)
            canvas.pack()
        elif self.direction == 2:
            canvas.move(self.icon, 0, 2)
            canvas.pack()
        elif self.direction == 3:
            canvas.move(self.icon, -2, 0)
            canvas.pack()
        if self.direction_timeout > 0:
            self.direction_timeout = self.direction_timeout - 1

    def get_coords(self):
        coords = canvas.coords(self.icon)
        if (self.direction == 1) or (self.direction == 3):
            x_add = 31
            y_add = 24
        else:
            x_add = 24
            y_add = 31
        coords.append(coords[0] + x_add)
        coords.append(coords[1] + y_add)
        return coords

    def kill(self):
        self.alive = False

    def get_alive(self):
        return self.alive

    def get_save_string(self):
        save_string = (str(canvas.coords(self.icon)[0]) + ' ' +
                       str(canvas.coords(self.icon)[1]) + ' ' +
                       str(self.direction) + ' ' +
                       str(self.alive)
                       )
        return save_string

    def smiley_cheat(self):
        self.up_image = PhotoImage(file='smiley.png')
        self.down_image = PhotoImage(file='smiley.png')
        self.left_image = PhotoImage(file='smiley.png')
        self.right_image = PhotoImage(file='smiley.png')
        canvas.itemconfig(self.icon, image=self.up_image)


class cBomb:
    def __init__(self, x, y, delay):
        self.coords = [x, y]
        self.timer = delay
        self.image = PhotoImage(file='bomb.png')
        self.icon = canvas.create_image(x - 10, y - 10,
                                        anchor='nw', image=self.image)

    def decrement_timer(self):
        self.timer = self.timer - 1

    def get_timer(self):
        return self.timer

    def get_coords(self):
        return self.coords

    def remove_bomb(self):
        canvas.delete(self.icon)

    def get_save_string(self):
        save_string = (str(self.coords[0]) + ' ' +
                       str(self.coords[1]) + ' ' +
                       str(self.timer))
        return save_string


class cBombTrail:
    def __init__(self, rectangles, timer):
        self.rectangles = rectangles
        self.timer = timer

    def decrement_timer(self):
        self.timer = self.timer - 1

    def remove_explosion(self):
        for i in range(len(self.rectangles)):
            canvas.delete(self.rectangles[i])

    def get_timer(self):
        return self.timer

    def get_save_string(self):
        save_string = str(self.timer)
        for rectangle in self.rectangles:
            rectangle_coords = canvas.coords(rectangle)
            for j in range(4):
                save_string = save_string + ' ' + str(rectangle_coords[j])
        return save_string

    @classmethod
    def create_from_save_file(cls, save_string):
        save_info = save_string.split(' ')
        index = 1
        save_rectangles = []
        for i in range(4):
            save_rectangles.append(canvas.create_rectangle
                                   (save_info[index],
                                    save_info[index + 1],
                                    save_info[index + 2],
                                    save_info[index + 3],
                                    fill='yellow',
                                    outline=''))
            index = index + 4
        return cls(save_rectangles, int(save_info[0]))


class cPillar:
    def __init__(self, x, y):
        self.pillar_img = PhotoImage(file='pillar.png')
        self.img = canvas.create_image(x, y, anchor='nw',
                                       image=self.pillar_img)
        self.x = x
        self.y = y

    def get_coords(self):
        return [self.x, self.y, self.x + 50, self.y + 50]


def create_window():  # create window and define size + position
    window = Tk()
    window.title('BaaBombs')
    ws = window.winfo_screenwidth()  # computers screen size
    hs = window.winfo_screenheight()
    x = (ws / 2) - (window_width / 2)  # calculate centre
    y = (hs / 2) - (window_height / 2)
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    window.resizable(False, False)
    return window


def overlapping(a_coords, b_coords):
    if a_coords[0] <= b_coords[2] and a_coords[2] >= b_coords[0] \
            and a_coords[1] <= b_coords[3] and a_coords[3] >= b_coords[1]:
        return True
    return False


def out_of_bounds(coords):
    if (coords[0] >= 0) and (coords[1] >= 0) \
            and (coords[2] <= window_width) \
            and (coords[3] <= window_height):
        return False
    else:
        return True


def create_world():
    bg = canvas.create_image(0, 0, anchor='nw', image=game_bg_image)
    canvas.tag_lower(bg)  # Sends image to back.
    x = 50
    y = 50
    for column in range(0, 5):
        for row in range(0, 5):
            pillars.append(cPillar(x, y))
            x += 100
        y += 100
        x = 50


def set_bomb(coords):
    bombs.append(
        cBomb((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2, 80))


def p1_set_bomb(event):
    set_bomb(p1_sheep.get_coords())


def p2_set_bomb(event):
    set_bomb(p2_sheep.get_coords())


def sheep_hit_by_explosion(sheep, rectangles):
    for i in range(len(rectangles)):
        if overlapping(canvas.coords(rectangles[i]), sheep.get_coords()):
            return True
    return False


def explode_bomb():
    bomb_coords = bombs[0].get_coords()
    bombs[0].remove_bomb()
    left_explosion = canvas.create_rectangle(bomb_coords[0] - 15,
                                             bomb_coords[1] - 15,
                                             bomb_coords[0],
                                             bomb_coords[1] + 15,
                                             fill='#ffe68c',
                                             outline='')
    explosion_left_width = 15
    collision = False
    while not collision:
        explosion_left_width = explosion_left_width + 2
        canvas.coords(left_explosion, bomb_coords[0] - explosion_left_width,
                      bomb_coords[1] - 15, bomb_coords[0],
                      bomb_coords[1] + 15)
        for i in range(len(pillars)):
            if overlapping(pillars[i].get_coords(),
                           canvas.coords(left_explosion)) or out_of_bounds(
                           canvas.coords(left_explosion)):
                collision = True

    right_explosion = canvas.create_rectangle(bomb_coords[0],
                                              bomb_coords[1] - 15,
                                              bomb_coords[0] + 15,
                                              bomb_coords[1] + 15,
                                              fill='#ffe68c', outline='')
    explosion_right_width = 15
    collision = False
    while not collision:
        explosion_right_width = explosion_right_width + 2
        canvas.coords(right_explosion, bomb_coords[0], bomb_coords[1] - 15,
                      bomb_coords[0] + explosion_right_width,
                      bomb_coords[1] + 15)
        for i in range(len(pillars)):
            if overlapping(pillars[i].get_coords(),
                           canvas.coords(right_explosion)) or out_of_bounds(
                           canvas.coords(right_explosion)):
                collision = True

    up_explosion = canvas.create_rectangle(bomb_coords[0] - 15,
                                           bomb_coords[1] - 15,
                                           bomb_coords[0] + 15,
                                           bomb_coords[1],
                                           fill='#ffe68c', outline='')
    explosion_up_height = 15
    collision = False
    while not collision:
        explosion_up_height = explosion_up_height + 2
        canvas.coords(up_explosion, bomb_coords[0] - 15,
                      bomb_coords[1] - explosion_up_height,
                      bomb_coords[0] + 15,
                      bomb_coords[1])
        for i in range(len(pillars)):
            if overlapping(pillars[i].get_coords(),
                           canvas.coords(up_explosion)) \
                    or out_of_bounds(canvas.coords(up_explosion)):
                collision = True

    down_explosion = canvas.create_rectangle(bomb_coords[0] - 15,
                                             bomb_coords[1],
                                             bomb_coords[0] + 15,
                                             bomb_coords[1] + 15,
                                             fill='#ffe68c', outline='')
    explosion_down_height = 15
    collision = False
    while not collision:
        explosion_down_height = explosion_down_height + 2
        canvas.coords(down_explosion,
                      bomb_coords[0] - 15,
                      bomb_coords[1],
                      bomb_coords[0] + 15,
                      bomb_coords[1] + explosion_down_height)
        for i in range(len(pillars)):
            if overlapping(pillars[i].get_coords(),
                           canvas.coords(down_explosion)) \
                    or out_of_bounds(canvas.coords(down_explosion)):
                collision = True
    if sheep_hit_by_explosion(p1_sheep,
                              [left_explosion, right_explosion,
                               up_explosion, down_explosion]):
        p1_sheep.kill()
    if sheep_hit_by_explosion(p2_sheep,
                              [left_explosion, right_explosion,
                               up_explosion, down_explosion]):
        p2_sheep.kill()
    bomb_trails.append(cBombTrail([right_explosion, left_explosion,
                                   up_explosion, down_explosion], 10))


def save_game():
    save_file = open('save_file.txt', 'w')
    save_file.write(p1_sheep.get_save_string() + '&' +
                    p2_sheep.get_save_string() + '/')
    for i in range(len(bombs)):
        save_file.write(bombs[i].get_save_string())
        if i != (len(bombs) - 1):
            save_file.write('&')
    save_file.write('/')
    for i in range(len(bomb_trails)):
        save_file.write(bomb_trails[i].get_save_string())
        if i != (len(bomb_trails) - 1):
            save_file.write('&')
    save_file.write('/')
    if game_over:
        save_file.write('Y')
    else:
        save_file.write('N')
    save_file.close()


def load_saved_game():  # Only loads sheep, bombs and bomb trails.
    save_file = open('save_file.txt', 'r')
    save_string = save_file.read()
    save_file.close()
    sections = save_string.split('/')
    sheep_saves = sections[0].split('&')
    global p1_sheep
    p1_sheep_save = sheep_saves[0].split(' ')
    if p1_sheep_save[3] == 'True':
        p1_sheep_alive = True
    else:
        p1_sheep_alive = False
    p1_sheep = cSheep(p1_sheep_save[0], p1_sheep_save[1],
                      int(p1_sheep_save[2]), p1_sheep_alive)
    global p2_sheep
    p2_sheep_save = sheep_saves[1].split(' ')
    if p2_sheep_save[3] == 'True':
        p2_sheep_alive = True
    else:
        p2_sheep_alive = False
    p2_sheep = cSheep(p2_sheep_save[0], p2_sheep_save[1],
                      int(p2_sheep_save[2]), p2_sheep_alive)
    if sections[1] != '':
        bomb_saves = sections[1].split('&')
        for bomb_save in bomb_saves:
            bomb_info = bomb_save.split(' ')
            bombs.append(cBomb(float(bomb_info[0]),
                               float(bomb_info[1]), int(bomb_info[2])))
    if sections[2] != '':
        bomb_trail_saves = sections[2].split('&')
        for trail in bomb_trail_saves:
            bomb_trails.append(cBombTrail.create_from_save_file(trail))
    global game_over
    if sections[3] == 'Y':
        game_over = True
    else:
        game_over = False
    os.remove('save_file.txt')


def essential_game_setup():
    global game_in_progress
    game_in_progress = True
    create_world()
    game_key_binds()
    global game_over
    game_over = False
    global smiley_cheat_tally
    smiley_cheat_tally = 0


def destroy_widgets():
    for widget in widgets:
        widget.destroy()
    widgets.clear()


def countdown():
    global pause_countdown
    canvas.pack()
    if pause_countdown > 0:
        canvas.delete('all')
        canvas.create_image(0, 0, image=menu_bg_image, anchor='nw')
        canvas.create_text(window_width / 2, window_height / 2,
                           fill='white', font='System 20 bold',
                           text=pause_countdown)
        pause_countdown -= 1
        canvas.after(1000, countdown)
    else:
        canvas.delete('all')
        global countdown_complete
        countdown_complete = True


def wait_to_unpause():
    global countdown_complete
    if countdown_complete:
        load_saved_game()
        essential_game_setup()
        play_game()
    else:
        canvas.after(1000, wait_to_unpause)


def unpause_game():
    canvas.delete('all')  # get rid of pause screen
    destroy_widgets()
    global pause_countdown
    pause_countdown = 3
    global countdown_complete
    countdown_complete = False
    countdown()
    wait_to_unpause()


def pause_game(event):
    global game_in_progress
    game_in_progress = False
    save_game()
    game_destroy()
    canvas.create_image(0, 0, image=menu_bg_image, anchor='nw')
    canvas.create_text(window_width / 2, window_height / 2,
                       fill='white', font='System 20 bold', text='Paused')
    widgets.append(Button(canvas, text='Unpause', command=unpause_game,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised'))
    widgets[0].place(x=window_width / 2 + 20, y=window_height / 2 + 30)
    widgets.append(Button(canvas, text='Save and Quit',
                          command=window.destroy,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised'))
    widgets[1].place(x=window_width / 2 - 100, y=window_height / 2 + 30)


def play_game():
    global game_over
    canvas.pack()
    if game_in_progress:
        if not game_over:
            p1_sheep_coords = p1_sheep.get_coords()
            p2_sheep_coords = p2_sheep.get_coords()
            for pillar in pillars:
                pillar_coords = pillar.get_coords()
                if overlapping(pillar_coords, p1_sheep_coords) \
                        or out_of_bounds(p1_sheep_coords) or overlapping(
                        p1_sheep_coords, p2_sheep_coords):
                    p1_sheep.reverse_dir()
                if overlapping(pillar_coords, p2_sheep_coords) \
                        or out_of_bounds(p2_sheep_coords) or overlapping(
                        p1_sheep_coords, p2_sheep_coords):
                    p2_sheep.reverse_dir()
            p1_sheep.move()
            p2_sheep.move()
            bomb_exploded = False
            for i in range(len(bombs)):
                bombs[i].decrement_timer()
                if i == 0 and bombs[0].get_timer() <= 0:
                    explode_bomb()
                    bomb_exploded = True
            if bomb_exploded:
                bombs.pop(0)
            trail_removed = False
            for i in range(len(bomb_trails)):
                bomb_trails[i].decrement_timer()
                if i == 0 and bomb_trails[i].get_timer() <= 0:
                    bomb_trails[i].remove_explosion()
                    trail_removed = True
            if trail_removed:
                bomb_trails.pop(0)
            if not (p1_sheep.get_alive() and p2_sheep.get_alive()):
                game_over = True
            window.after(20, play_game)
        else:
            bomb_trails[0].decrement_timer()
            if bomb_trails[0].get_timer() <= 0:
                bomb_trails[0].remove_explosion()
                game_end()
            else:
                window.after(20, play_game)


def smiley_cheat(event):
    global smiley_cheat_tally
    if smiley_cheat_tally == 5:
        p1_sheep.smiley_cheat()
        p2_sheep.smiley_cheat()
    smiley_cheat_tally += 1


def game_key_binds():
    window.bind('<Left>', p2_sheep.go_west)
    window.bind('a', p1_sheep.go_west)
    window.bind('<Right>', p2_sheep.go_east)
    window.bind('d', p1_sheep.go_east)
    window.bind('<Up>', p2_sheep.go_north)
    window.bind('w', p1_sheep.go_north)
    window.bind('<Down>', p2_sheep.go_south)
    window.bind('s', p1_sheep.go_south)
    window.bind('<Return>', p2_set_bomb)
    window.bind('e', p1_set_bomb)
    window.bind('<space>', pause_game)
    window.bind('`', smiley_cheat)
    window.bind('<F9>', boss_key)


def unbind_game_keys():
    window.unbind('<Left>')
    window.unbind('a')
    window.unbind('<Right>')
    window.unbind('d')
    window.unbind('<Up>')
    window.unbind('w')
    window.unbind('<Down>')
    window.unbind('s')
    window.unbind('<Return>')
    window.unbind('e')
    window.unbind('<space>')
    window.unbind('`')
    window.unbind('<F9>')


def reset_sheep():
    global p1_sheep
    p1_sheep = cSheep(10, 10, -1, True)
    global p2_sheep
    p2_sheep = cSheep(510, 510, -1, True)


def new_game():
    reset_sheep()
    essential_game_setup()
    play_game()


def game_restart():
    canvas.delete('all')
    destroy_widgets()
    new_game()


def game_destroy():
    unbind_game_keys()
    bombs.clear()
    bomb_trails.clear()
    pillars.clear()
    canvas.delete('all')
    global p1_sheep
    del p1_sheep
    global p2_sheep
    del p2_sheep


def get_score_file_contents():
    if not os.path.exists('scoreboard.txt'):
        score_file = open('scoreboard.txt', 'x')
        score_file.close()
        return ''
    score_file = open('scoreboard.txt', 'r')
    score_file_string = score_file.read()
    score_file.close()
    return score_file_string


def display_scoreboard():
    canvas.delete('all')
    destroy_widgets()
    canvas.create_image(0, 0, image=menu_bg_image, anchor='nw')
    canvas.create_text(window_width / 2, 50,
                       fill='white',
                       font='System 30 bold',
                       text='Leaderboard',
                       anchor='center')
    canvas.create_text(100, 90,
                       fill='white',
                       font='System 20 bold',
                       text='NICKNAME',
                       anchor='nw')
    canvas.create_text(350, 90,
                       fill='white',
                       font='System 20 bold',
                       text='WINS',
                       anchor='nw')
    score_file_string = get_score_file_contents()
    entries = score_file_string.split('/')
    scores = ''
    names = ''
    # limit number of scores displayed to top 15
    if len(entries) < 16:
        max_names = len(entries)
    else:
        max_names = 16
    for i in range(1, max_names):
        # Starts at one because the first data item is an empty string.
        current_highest_score = 0
        for j in range(1, len(entries)):
            data = entries[j].split(' ')
            if current_highest_score < int(data[1]):
                current_highest_score = int(data[1])
                ch_name = data[0]
                ch_index = j
        entries[
            ch_index] = 'x 0'  # Prevents the same entry being counted again.
        names = names + ch_name + '\n'
        scores = scores + str(current_highest_score) + '\n'
    canvas.create_text(100, 150,
                       fill='white', font='System 15 bold', text=names,
                       anchor='nw')
    canvas.create_text(350, 150,
                       fill='white', font='System 15 bold', text=scores,
                       anchor='nw')
    widgets.append(Button(canvas, text='New Game', command=game_restart,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised'))
    widgets[0].place(x=30, y=30)
    widgets.append(Button(canvas, text='Main Menu', command=display_menu,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised'))
    widgets[1].place(x=520, y=30, anchor='ne')


def add_to_scoreboard():
    nick = widgets[1].get()
    nick = nick.lower()
    score_file_string = get_score_file_contents()
    entries = score_file_string.split('/')
    score_file_string = ''
    nick_found = False
    for i in range(1, len(entries)):
        # Starts at one because the first data item is an empty string.
        data = entries[i].split(' ')
        if data[0] == nick:
            nick_found = True
            data[1] = str(int(data[1]) + 1)
            entries[i] = data[0] + ' ' + data[1]
        score_file_string = score_file_string + '/' + entries[i]
    if not nick_found:
        score_file_string = score_file_string + '/' + nick + ' 1'
    score_file = open('scoreboard.txt', 'w')
    score_file.write(score_file_string)
    score_file.close()


def add_to_scoreboard_btn():
    nick = widgets[1].get()
    nick = nick.lower()
    valid_letters = 'qwertyuiopasdfghjklzxcvbnm'
    valid_nick = True
    if nick == '':
        valid_nick = False
    for i in range(len(nick)):
        if nick[i] not in valid_letters:
            valid_nick = False
    if valid_nick:
        add_to_scoreboard()
        display_scoreboard()
    else:
        canvas.create_text(window_width / 2, window_height / 2 + 70,
                           fill='red', font='System 10 bold',
                           text='Nickname must be letters only!')


def game_end():
    if not p1_sheep.get_alive():
        if not p2_sheep.get_alive():
            winner = -1
        else:
            winner = 2
    else:
        winner = 1
    game_destroy()
    canvas.create_image(0, 0, image=menu_bg_image, anchor='nw')
    if winner == 1:
        canvas.create_text(window_width / 2, (window_height / 2) - 100,
                           fill='white', font='System 20 bold',
                           text='Player 1 wins')
    elif winner == 2:
        canvas.create_text(window_width / 2, (window_height / 2) - 100,
                           fill='white', font='System 20 bold',
                           text='Player 2 wins')
    else:
        canvas.create_text(window_width / 2, (window_height / 2) - 100,
                           fill='white', font='System 20 bold',
                           text='Draw')
    widgets.append(Button(canvas, text='Play Again', command=game_restart,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised'))
    widgets[0].place(x=window_width / 2, y=window_height / 2 + 200,
                     anchor='center')
    if winner == 1 or winner == 2:
        canvas.create_text(window_width / 2, (window_height / 2), fill='white',
                           font='System 15 bold',
                           text="Enter winning player's nickname:")
        widgets.append(Entry(canvas))
        widgets[1].place(x=window_width / 2, y=window_height / 2 + 30,
                         anchor='center')
        widgets.append(Button(canvas, text='Add to scoreboard',
                              command=add_to_scoreboard_btn,
                              bg='#4D9629', font='System', fg='white',
                              relief='flat', overrelief='raised'))
        widgets[2].place(x=window_width / 2, y=window_height / 2 + 100,
                         anchor='center')


def yes_load_button_pressed():
    canvas.delete('all')
    destroy_widgets()
    global pause_countdown
    pause_countdown = 3
    global countdown_complete
    countdown_complete = False
    countdown()
    wait_to_unpause()


def no_load_button_pressed():
    os.remove('save_file.txt')
    canvas.delete('all')
    destroy_widgets()
    new_game()


def return_after_boss_key(event):
    window.unbind('<F8>')
    window.bind('<F9>', boss_key)
    canvas.delete('all')
    load_saved_game()
    essential_game_setup()
    play_game()


def boss_key(event):
    window.unbind('<F9>')
    window.bind('<F8>', return_after_boss_key)
    global game_in_progress
    if game_in_progress:
        save_game()
        game_destroy()
    game_in_progress = False
    fake_work = canvas.create_image(0, 0, anchor='nw', image=fake_work_img)


def return_from_tutorial():
    window.unbind('<Enter>')
    canvas.delete('all')
    destroy_widgets()
    display_menu()


def how_to_play_btn():
    destroy_widgets()
    canvas.delete('all')
    canvas.create_image(0, 0, image=menu_bg_image, anchor='nw')
    canvas.create_text(window_width / 2, window_height / 2 - 150,
                       fill='white', font='System 30 bold',
                       text='How To Play')
    canvas.create_text(window_width / 2, window_height / 2 - 100, fill='white',
                       font='System 10 bold',
                       text="This game is for two players.\nTry to explode "
                            "your opponent's sheep\nwhile not getting exploded"
                            " yourself!\n\nPlayer 1 controls:\nWASD keys to "
                            "move\nE to place bomb\n\nPlayer 2 controls:\n"
                            "Arrow keys to move\nEnter key to place bomb"
                            "\n\nBoss Key: F9 (F8 to return to game)",
                       anchor='n')
    canvas.create_text(20, window_height / 2 + 250, fill='dark green',
                       font='System 10',
                       text="Press the ` key 6 times or type in 'hi' for "
                            "fun suprises :)", anchor='nw')
    widgets.append(Button(canvas, text='Back', command=return_from_tutorial,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised'))
    widgets[0].place(x=540, y=540, anchor='se')


def start_btn():
    destroy_widgets()
    canvas.delete('all')
    new_game()


def leaderboard_btn():
    destroy_widgets()
    canvas.delete('all')
    display_scoreboard()


def display_menu():
    canvas.delete('all')
    destroy_widgets()
    canvas.create_image(0, 0, image=main_menu_bg_image, anchor='nw')
    widgets.append(Button(canvas, text='Start', command=start_btn,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised', width=15))
    widgets[0].place(x=window_width / 2, y=window_height / 2 - 30,
                     anchor='center')
    widgets.append(Button(canvas, text='How To Play', command=how_to_play_btn,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised', width=15))
    widgets[1].place(x=window_width / 2, y=window_height / 2, anchor='center')
    widgets.append(Button(canvas, text='Leaderboard', command=leaderboard_btn,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised', width=15))
    widgets[2].place(x=window_width / 2, y=window_height / 2 + 30,
                     anchor='center')
    canvas.pack()


def hi_cheat_h(event):
    global h_pressed
    h_pressed = True


def hi_cheat_i(event):
    global h_pressed
    if h_pressed:
        hi_text = canvas.create_text(20, 20, fill='white',
                                     font='System 10 bold',
                                     text='i hope you like my game! :)\n'
                                          'Credits:\nProgramming: me\n'
                                          'Graphics: also me\n'
                                          'Special thanks to: Caffeine',
                                     anchor='nw')
        h_pressed = False


game_in_progress = False
window_width = 550
window_height = 550
window = create_window()
window.configure(bg='black')
canvas = Canvas(window, bg='#9ECC66', highlightthickness=0,
                width=window_width, height=window_height)
fake_work_img = PhotoImage(file='fake_work.png')
menu_bg_image = PhotoImage(file='bg.png')
main_menu_bg_image = PhotoImage(file='main_menu_bg.png')
game_bg_image = PhotoImage(file='grass.png')
bombs = []
pillars = []
bomb_trails = []
widgets = []
window.bind('h', hi_cheat_h)
window.bind('i', hi_cheat_i)
h_pressed = False
canvas.focus_set()

if os.path.exists('save_file.txt'):
    canvas.create_image(0, 0, image=menu_bg_image, anchor='nw')
    save_text_1 = canvas.create_text(window_width / 2,
                                     window_height / 2,
                                     fill='white',
                                     font='System 20 bold',
                                     text='Saved game detected.')
    save_text_2 = canvas.create_text(window_width / 2, window_height / 2 + 30,
                                     fill='white', font='System 20 bold',
                                     text='Load game?')
    widgets.append(Button(canvas, text='Yes',
                          command=yes_load_button_pressed,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised'))
    widgets[0].place(x=window_width / 2 - 30, y=window_height / 2 + 60,
                     anchor='ne')
    widgets.append(Button(canvas, text='No', command=no_load_button_pressed,
                          bg='#4D9629', font='System', fg='white',
                          relief='flat', overrelief='raised'))
    widgets[1].place(x=window_width / 2 + 30, y=window_height / 2 + 60,
                     anchor='nw')
    canvas.pack()
else:
    display_menu()

window.mainloop()
