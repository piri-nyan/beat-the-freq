import tkinter
from modules.UI import Window
from modules.game import Host

def main():
    root = tkinter.Tk()
    root.title("Beat the Freq")
    window = Window(root)
    game_host = Host(window)
    window.set_game_host(game_host)

    root.mainloop()

if __name__=="__main__":
    main()