import pygame
import random


def help_menu():
    print("Press Esc to quit.")
    print("Press H to reprint this help menu.")
    print("Press N to generate population.")
    print("Press P to display population.")
    print("Press C to set an environment color.")  # in the future generate a complex environment
    print("Press E to display environment color")
    print("Press S to save data to file. ")
    print("Press L to load data from file. ")


print("Welcome to Evolution Simulator!", end='\n\n')
help_menu()

screen = pygame.display.set_mode((500, 500))
screen.fill((255, 255, 255))
pygame.display.set_caption("Evolution Simulator")
running = True
entering_bg_color = False
environment_color = ""
colors_saved = [[] for i in range(500)]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            if entering_bg_color:
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or \
                    event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or \
                    event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9 or \
                    event.key == pygame.K_0 or event.key == pygame.K_a or event.key == pygame.K_b or \
                    event.key == pygame.K_c or event.key == pygame.K_d or event.key == pygame.K_e or \
                        event.key == pygame.K_f:
                    if len(environment_color) < 6:
                        environment_color += event.unicode
                        print("'\r{0}".format(environment_color), end='')
                elif event.key == pygame.K_BACKSPACE:
                    environment_color = environment_color[:-1]
                    print("'\r{0}".format(environment_color), end='')
                elif event.key == pygame.K_RETURN:
                    entering_bg_color = False
                    print("Creating environment using hexcode (0x" + '\033[1m' + environment_color + '\033[0m' + ")...")
                    try:
                        environment_color = tuple(int(environment_color[i:i + 2], 16) for i in (0, 2, 4))
                    except ValueError:
                        environment_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        print("Invalid hexcode, using random RGB value " + str(environment_color) + "...")
                    finally:
                        print("Set.")

            elif event.key == pygame.K_h:
                help_menu()
                pass
            elif event.key == pygame.K_n:
                print("Populating...")
                colors_saved = [[] for i in range(500)]
                i = 0
                while i < 500:
                    j = 0
                    while j < 500:
                        z = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        colors_saved[i].append(z)
                        j += 1
                    i += 1
                print("Finished populating.")
            elif event.key == pygame.K_p:
                print("Displaying population...")
                k = 0
                for i in colors_saved:
                    m = 0
                    for j in i:
                        screen.set_at((k, m), j)
                        m += 1
                    k += 1
                print("Displayed.")
            elif event.key == pygame.K_c:
                print("Enter environment color in hexadecimal (ex. 95bf39 is lime)")
                environment_color = ""
                entering_bg_color = True
            elif event.key == pygame.K_e:
                print("Displaying environment...")
                screen.fill(environment_color)
                print("Displayed.")
            elif event.key == pygame.K_s:
                print("Saving...")
                with open("savefile.txt", "w") as txt_file:
                    for line in colors_saved:
                        txt_file.write("".join(str(line)) + "\n")
                    txt_file.write(str(environment_color))
                    print("Finished.")
                    txt_file.close()
            elif event.key == pygame.K_l:
                print("Loading...")
                colors_saved = [[] for i in range(500)]
                try:
                    with open("savefile.txt", "r") as txt_file:
                        lines = txt_file.read().split('\n')
                        environment_color = eval(lines[-1])
                        lines.pop(-1)
                        i = 0
                        for temp_format in lines:
                            tuples = temp_format.split('), (')
                            tuples[0] = tuples[0][2:]
                            tuples[-1] = tuples[-1][:-2]
                            for pixel in tuples:
                                colors_saved[i].append(eval(pixel))
                            i += 1
                        print("Loaded.")
                        txt_file.close()
                except FileNotFoundError:
                    print("Save file not found.")
                except SyntaxError:
                    print("Incorrect file type.")

    pygame.display.flip()


# TODO: make the actual sim lol
# if a pixel is a certain shade, allow it to infect all 8 of its surrounding pixels - disease
