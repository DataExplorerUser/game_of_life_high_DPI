import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from threading import Thread
from time import sleep
import ctypes

# set DPI awareness on Windows to High DPI awareness for better font rendering
ctypes.windll.shcore.SetProcessDpiAwareness(2)

global columnAmt
global rowAmt
columnAmt = 50
rowAmt = 30

colorsId = []
nextFrame = []

configuration = []

simSpeed = 0.20
running = False

wrappingLR = True
wrappingTD = True

def load_fonts():
    # add fonts to font registry
    with dpg.font_registry():
        # add font (set as default for entire app)
        default_font = dpg.add_font(tag='font1', file='fonts/readerpro/readerpro_medium.ttf', size=24)
        dpg.bind_font(default_font)

        # add font for increasing the height of the widgets
        big_font = dpg.add_font(tag='font2', file='fonts/readerpro/readerpro_medium.ttf', size=36)

        # add font for increasing the height of the widgets
        logo_font = dpg.add_font(tag='font3', file='fonts/lobster/lobster-regular.ttf', size=72)

    # set up theme for window rounding
    with dpg.theme() as theme:
        with dpg.theme_component():
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
    dpg.bind_theme(theme)

    color_orange = (217, 131, 46)
    color_green = (70, 140, 40)
    color_black = (0, 0, 0)
    color_grey = (40, 40, 40)
    color_orange_muted = (217, 131, 46, 200)
    color_light_green = (98, 190, 67)
    color_white = (200, 200, 200)

    with dpg.theme(tag='inactive_button_theme'):
        with dpg.theme_component():
            dpg.add_theme_color(dpg.mvThemeCol_Button, color_black, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, color_green, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, color_light_green, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag='active_button_theme'):
        with dpg.theme_component():
            dpg.add_theme_color(dpg.mvThemeCol_Button, color_white, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, color_green, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, color_light_green, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag='controller_button_theme'):
        with dpg.theme_component():
            dpg.add_theme_color(dpg.mvThemeCol_Button, color_grey, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, color_orange_muted, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, color_orange, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 15, category=dpg.mvThemeCat_Core)


def get_near_cells_amount(cell):
    # get the cells near another one, and returns the count of live cells
    topLeft, top, topRight, left, right, bottomLeft, bottom, bottomRight = [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]

    # temp
    print('topleft:', (cell[0] - 1) % columnAmt )
    print('topleft:', (cell[1] - 1) % rowAmt)
    # print('topleft:', colorsId[39][59])  # --> x and y are switched


    if cell[1] != 0:
        top = colorsId[(cell[0] - 0)][(cell[1] - 1)]
    if cell[1] != rowAmt - 1:
        bottom = colorsId[(cell[0] - 0)][(cell[1] + 1)]
    if cell[0] != 0:
        left = colorsId[(cell[0] - 1)][(cell[1] - 0)]
    if cell[0] != columnAmt - 1:
        right = colorsId[(cell[0] + 1)][(cell[1] - 0)]
    if cell[0] != 0 and cell[1] != 0:
        topLeft = colorsId[(cell[0] - 1)][(cell[1] - 1)]
    if cell[0] != 0 and cell[1] != rowAmt - 1:
        bottomLeft = colorsId[(cell[0] - 1)][(cell[1] + 1)]
    if cell[0] != columnAmt - 1 and cell[1] != 0:
        topRight = colorsId[(cell[0] + 1)][(cell[1] - 1)]
    if cell[0] != columnAmt - 1 and cell[1] != rowAmt - 1:
        bottomRight = colorsId[(cell[0] + 1)][(cell[1] + 1)]

    if wrappingTD:
        topLeft = colorsId[(cell[0] - 1) % columnAmt][(cell[1] - 1) % rowAmt]
        top = colorsId[(cell[0] - 0) % columnAmt][(cell[1] - 1) % rowAmt]
        topRight = colorsId[(cell[0] + 1) % columnAmt][(cell[1] - 1) % rowAmt]
        bottomLeft = colorsId[(cell[0] - 1) % columnAmt][(cell[1] + 1) % rowAmt]
        bottom = colorsId[(cell[0] - 0) % columnAmt][(cell[1] + 1) % rowAmt]
        bottomRight = colorsId[(cell[0] + 1) % columnAmt][(cell[1] + 1) % rowAmt]

    if wrappingLR:
        topLeft = colorsId[(cell[0] - 1) % columnAmt][(cell[1] - 1) % rowAmt]
        left = colorsId[(cell[0] - 1) % columnAmt][(cell[1] - 0) % rowAmt]
        bottomLeft = colorsId[(cell[0] - 1) % columnAmt][(cell[1] + 1) % rowAmt]
        topRight = colorsId[(cell[0] + 1) % columnAmt][(cell[1] - 1) % rowAmt]
        right = colorsId[(cell[0] + 1) % columnAmt][(cell[1] - 0) % rowAmt]
        bottomRight = colorsId[(cell[0] + 1) % columnAmt][(cell[1] + 1) % rowAmt]

    near_cells = topLeft, top, topRight, left, right, bottomLeft, bottom, bottomRight

    return list(i[1] for i in near_cells).count(1)


def gen_life(cell):
    """
    RULES
    Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any live cell with more than three live neighbours dies, as if by overpopulation.
    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    amt = get_near_cells_amount(cell)
    data = colorsId[cell[0]][cell[1]]  # [id, isAlive]

    if data[1] is True and amt < 2:
        nextFrame.append(data[0])
    elif data[1] is True and (amt == 2 or amt == 3):
        pass
    elif data[1] is True and amt > 3:
        nextFrame.append(data[0])
    elif data[1] is False and amt == 3:
        nextFrame.append(data[0])


def update():
    print('updating')
    for i in range(columnAmt):
        for j in range(rowAmt):
            print(i, j)
            print(get_near_cells_amount([i, j]))
            if get_near_cells_amount([i, j]) != 0 or colorsId[i][j][1]:
                gen_life([i, j])

    # after getting the frame situation, apply it
    for i in nextFrame:
        change_color(0, i)
        print(i)

    nextFrame.clear()


def run():
    # thread function, starts the simulation in another thread
    dpg.set_value("RUNNING_SIMULATION_TEXT", "Running")
    dpg.configure_item("RUNNING_SIMULATION_TEXT", color=[20, 200, 20])
    while running:
        update()
        sleep(simSpeed)


def start_sim():
    global running

    # starts the simulation
    if not running:
        running = True
        Thread(target=run, daemon=True).start()
    else: # When is this condition triggered? Does not seem to occur at all.
        running = False
        dpg.set_value("RUNNING_SIMULATION_TEXT", "Stopped")
        dpg.configure_item("RUNNING_SIMULATION_TEXT", color=[217, 131, 46]) # red [200, 30, 20]


def next_frame():
    # generate the next frame only
    if running is False:
        update()


def clear_board():
    for i in range(columnAmt):
        for j in range(rowAmt):
            if colorsId[i][j][1]:
                change_color(0, colorsId[i][j][0])


def stop_sim():
    # stop the simulation
    global running
    running = False

    # set texts
    dpg.set_value("RUNNING_SIMULATION_TEXT", "Stopped")
    dpg.configure_item("RUNNING_SIMULATION_TEXT", color=[217, 131, 46])

    clear_board()


def save():
    global configuration
    configuration = [[[k for k in j] for j in i] for i in colorsId]


def load():
    global colorsId

    clear_board()

    # load config
    for i in range(columnAmt):
        for j in range(rowAmt):
            if configuration[i][j][1]:
                change_color(0, configuration[i][j][0])


def button_click(sender, app_data, user_data):
    print('sender:', sender, '| appdata:', app_data, '| user_data:', user_data)
    # change_color(user_data)
    # SET BUTTON THEME BUTTON
    dpg.bind_item_theme(item=sender, theme='active_button_theme')

def change_color(data): # data=(0,i)  -

    # REPLACE FOLLOWING SECTION WITH THEME SETTING
    # set color
    # v = dpg.get_value(data[1])
    # dpg.set_value(data[1], [255 - v[0], 255 - v[1], 255 - v[2]])

    # SET BUTTON THEME BUTTON
    # dpg.bind_item_theme(item=, theme='active_button_theme')

    # change value on 2D - array
    cell = dpg.get_item_user_data(data[1])
    colorsId[cell[0]][cell[1]][1] = not colorsId[cell[0]][cell[1]][1]


def pause_sim():
    # pauses the simulation
    global running
    running = False
    dpg.set_value("RUNNING_SIMULATION_TEXT", "Stopped")
    dpg.configure_item("RUNNING_SIMULATION_TEXT", color=[200, 30, 20])


def change_sim_speed(s, data):
    # changes the simulation speed
    global simSpeed

    data = 10 ** data
    simSpeed = 1 / data
    dpg.set_value(item='speedometer', value=f"{round(data, 2)}")

def set_wrapping(s, data):
    # set the wrapping option
    global wrappingLR, wrappingTD
    if "LR" in dpg.get_item_label(s):
        wrappingLR = data
    elif "TD" in dpg.get_item_label(s):
        wrappingTD = data


def main():

    with dpg.window() as main_window:
        dpg.set_primary_window(main_window, True)

        # header
        with dpg.child_window(width=1000, height=60):
            dpg.add_spacer(height=40)
            # dpg.add_text(tag='logo', default_value="""Conway's Game of Life""", indent=500, color=(100,100,100))
            # dpg.bind_item_font(item='logo', font='font3')

        with dpg.group(horizontal=True): # contains game board and control panel

            dpg.add_spacer(width=70) # space between viewport and game board

            # fill game board with square buttons
            with dpg.child_window(width=1370, height=(25+5)*(rowAmt), no_scrollbar=True) as game_board:
                for y in range(0, rowAmt):
                    temp = []
                    with dpg.group(horizontal=True, horizontal_spacing=2):
                        for x in range(0, columnAmt):
                            new_button_id = dpg.add_button(label='', width=25, height=25, callback=button_click, user_data=[x, y])
                            temp.append([new_button_id, False])
                    colorsId.append(temp)
                    configuration.append(temp)

            # give all buttons the inactive color
            dpg.bind_item_theme(game_board, 'inactive_button_theme')

            with dpg.child_window(width=450, height=800) as control_window:
                dpg.bind_item_theme(control_window, 'controller_button_theme')

                dpg.add_text('Simulation controls', indent=120)
                dpg.add_spacer(height=15)
                dpg.add_button(label="Start / Pause", callback=start_sim, height=40, width=300, indent=65)
                dpg.add_spacer(height=10)
                dpg.add_button(label="Stop / Clear", callback=stop_sim, height=40, width=300, indent=65)
                dpg.add_spacer(height=10)
                dpg.add_button(label="Next Frame", callback=next_frame, height=40, width=300, indent=65)
                dpg.add_spacer(height=20)
                dpg.add_checkbox(label="TD Wrapping", default_value=True, callback=set_wrapping, indent=65)
                dpg.add_spacer(height=10)
                dpg.add_checkbox(label="LR Wrapping", default_value=True, callback=set_wrapping, indent=65)
                dpg.add_spacer(height=10)
                dpg.add_slider_int(label="TD Toggle", default_value=0, format='', callback=set_wrapping, width=50,
                                   height=80, max_value=1, indent=65)
                dpg.add_spacer(height=20)
                dpg.add_button(label="Save Board", callback=save, height=40, width=300, indent=65)
                dpg.add_spacer(height=10)
                dpg.add_button(label="Load Board", callback=load, height=40, width=300, indent=65)

                dpg.add_spacer(height=20)
                dpg.add_text("Status", indent=65)
                dpg.add_text("Initialization", color=[217, 131, 46], tag="RUNNING_SIMULATION_TEXT", indent=65)

                dpg.add_spacer(height=20)

                dpg.add_text('Speed', indent=65)
                dpg.add_text("Speed 0.699", tag='speedometer', indent=65)
                dpg.add_spacer(height=10)
                dpg.add_slider_float(tag='slider', label='', min_value=0, max_value=2, width=300, default_value=0.699,
                                     callback=change_sim_speed,
                                     format='', indent=65)  # format=f"Simulation Speed: x{round(10 ** 0.699, 2)}"
                dpg.add_spacer(height=10)
                dpg.bind_item_font(item='slider', font='font2')  # bind bigger font to slider to increase slider height

                dpg.add_spacer(height=20)
                dpg.add_text('Iteration: 0', indent=65)


if __name__ == '__main__':

    width = 1920
    height = 1080

    dpg.create_context()
    dpg.create_viewport(width=width, max_width=width, min_width=width, height=height, min_height=height, max_height=height, resizable=False, title="DPG Conway's Game Of Life version 1", large_icon="src/GMF.ico", small_icon="src/GMF.ico")
    dpg.setup_dearpygui()
    load_fonts()
    main()

    # demo.show_demo()
    # dpg.show_style_editor()

    # switching rows and columns count to offset the switcheroo when creating the game_board
    new_rowAmt = columnAmt
    columnAmt = rowAmt
    rowAmt = new_rowAmt

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
