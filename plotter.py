import matplotlib.pyplot as plt
import numpy as np
import socket

s = socket.socket()
port = 5050
maxConnections = 5
IP = socket.gethostname()

s.bind(('', port))

s.listen(maxConnections)
print("Server started at " + IP + " on port " + str(port))

clientsocket, address = s.accept()
print("Connection made")

# use ggplot style for more sophisticated visuals
plt.style.use('dark_background')


def live_plotter(x_vec, y1_data, line_1, identifier='', pause_time=0.000000001):
    if line_1 == []:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line_1, = ax.plot(x_vec, y1_data, '-o', alpha=0.8)
        # update plot label/title
        plt.ylabel('Error Value')
        plt.title('Y axis Error'.format(identifier))
        plt.show()

    # after the figure, axis, and line are created, we only need to update the y-data
    line_1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data) <= line_1.axes.get_ylim()[0] or np.max(y1_data) >= line_1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line_1


size = 100
x_vec = np.linspace(0, 1, size + 1)[0:-1]
y_vec_1 = np.random.randn(len(x_vec))
y_vec_2 = np.random.randn(len(x_vec))
line1 = []
line2 = []

while True:

    try:
        message = clientsocket.recv(1024).decode()

        if message != "":
            message = message.replace("(", "")
            message = message.replace(")", "")
            message = message.split(",")
            message = int(message[0]), int(message[1])

        if abs(message[1]) < 400:
            rand_val = np.random.randn(1)
            y_vec_1[-1] = -message[1]
            line1 = live_plotter(x_vec, y_vec_1, line1)
            y_vec_1 = np.append(y_vec_1[1:], 0.0)

    except:
        pass
