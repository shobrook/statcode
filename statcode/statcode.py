#########
# GLOBALS
#########


import os
import sys


from statcode.app_handler import App
from statcode.content_generator import get_yaml_dictionary, generate_content

#########
# HELPERS
#########
from statcode.constants import SCROLL_LINE_UP, SCROLL_LINE_DOWN, SCROLL_PAGE_UP, SCROLL_PAGE_DOWN, SCROLL_TO_END, \
    END, RED, BOLD, CURR_DIR, SCROLL_TO_TOP, UNDERLINE, YELLOW

######
# MAIN
######

## Helpers ##


def print_help():
    print(''.join([BOLD, "httphelp v1.1.0 – Made by @Malex", END, '\n']))
    print(''.join([BOLD, "Based on statcode v1.0.0 – Made by @shobrook", END, '\n']))
    print("Like man pages, but for HTTP status codes and headers (and more).\n")
    print(''.join([UNDERLINE, "Usage:", END, " $ statcode ", YELLOW, "status_code", END]))
    print(''.join([BOLD, "-h, --help:", END, " prints this help"]))
    print(''.join([BOLD, "-a,-l, --all,--list statucode", END, " prints all codes in compact version"]))
    print(''.join([BOLD, "-a,-l, --all,--list headers", END, " prints all headers in compact version"]))


def print_all(status_code):
    if status_code == "statuscode":
        code_descriptions, num, status_code = get_yaml_dictionary(200)
    else:
        code_descriptions, num, status_code = get_yaml_dictionary("Accept")
    del status_code
    for k, v in code_descriptions.items():
        print(''.join([RED, str(k), ':', END, " ", v["message"] if num else ""]))


## Main ##


def main():
    if len(sys.argv) == 1 or sys.argv[1].lower() in ("-h", "--help"):
        print_help()
    elif sys.argv[1].lower() in ("-a", "-l", "--all", "--list"):
        try:
            status_code = sys.argv[2]
            if status_code not in ("statuscode", "headers"):
                print(''.join([BOLD, "Wrong parameter for this usage, see help", END]))
                return
            print_all(status_code)
        except IndexError:
            print_help()
    else:
        status_code = sys.argv[1]
        content = generate_content(status_code)

        if content:
            try:
                App(content)  # Opens interface
            except NameError:
                size = os.get_terminal_size()
                canvas = content.render(size)
                text = "".join(text.decode("utf-8") for text in canvas.text)
                print(text.rstrip())
        else:
            print(''.join([RED, "Sorry, statcode doesn't recognize: ", status_code, END]))

    return
