from tkinter import *
import serial

def start_connection():
    BAUD_RATE = 9600
    TIMEOUT = 1.0 # 1 second
    PORT = '/dev/tty.usbmodem11301' # depends on the unit running rsudp; can be "COM3" when on windows; entirely machine-dependent

    print('Opening a serial connection on PORT %s with BAUD RATE %d and TIMEOUT in %d second(s)' % (PORT, BAUD_RATE, TIMEOUT))
    ser = serial.Serial(PORT, BAUD_RATE)
    return ser

def send_signal(ser, signal):
    print('Sending signal: %s' % signal)
    ser.write(b'%s' % bytes(signal, 'utf-8'))

def handle_close(ser, root):
    print('Closing serial connection...')
    ser.close()
    print('Destroy tkinter instance...')
    root.destroy()

window = Tk()
window.geometry("600x300")
window.title("Alarm Interface")
ser = start_connection()

label = Label(window, text="Alarm Trigger",font=('Arial',40, 'bold'),fg='white')
label.pack()

high_signal_btn = Button(window, text="ABOVE THRESHOLD", command=lambda: send_signal(ser, "HIGH"), bg="blue")
high_signal_btn.place(x=50, y=150)
high_signal_btn.pack()

low_signal_btn = Button(window, text="BELOW THRESHOLD", command=lambda: send_signal(ser, "LOW"), bg="blue")
low_signal_btn.place(x=50, y=250)
low_signal_btn.pack()

window.protocol("WM_DELETE_WINDOW", lambda: handle_close(ser, window))
window.mainloop()
