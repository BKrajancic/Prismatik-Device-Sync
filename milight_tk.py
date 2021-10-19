
import colorsys
import milight
import tkinter
import socket

def _main():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("127.0.0.1", 3636))
    connection.recv(8192)

    light = milight.load_milight("192.168.0.92", 8899, 4)

    root = tkinter.Tk()
    root.title("Drawer")
    width = 1080
    height = 300
    canvas = tkinter.Canvas(root, width=width, height=height, bg="black")
    def _update_canvas():
        update_canvas(light, connection, width, height, canvas)

    button = tkinter.Button(
        root,
        text="Hello",
        fg="red",
        command= _update_canvas
    )
    button.pack()

    root.mainloop()

def update_canvas(light, connection, width, height, canvas: tkinter.Canvas):
    canvas.delete("all")
    leds = list(zip(*milight.get_leds(connection)))

    square_size = round(width / len(leds))
    for i, led in enumerate(leds):
        color = "#{:02x}{:02x}{:02x}".format(int(led[0]), int(led[1]), int(led[2]))
        box = canvas.create_rectangle(
            i * square_size, 0, 
            (i * square_size) + square_size, height // 2,
            fill=color,
            tags="all"
        )
    hue, saturation, val = milight._get_average_rgb(connection)

    milight.transmit_color(light, 4, hue, saturation, val)
    rgb =  colorsys.hsv_to_rgb(hue, saturation, val)
    average_color = "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255),
        int(rgb[1] * 255),
        int(rgb[2] * 255)
    )

    box = canvas.create_rectangle(
        0, height // 2, 
        width, height,
        fill=average_color
    )
    canvas.pack()




if __name__ == "__main__":
    _main()