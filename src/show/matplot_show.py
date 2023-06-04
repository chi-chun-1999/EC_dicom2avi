import matplotlib.pyplot as plt


def matplot_show_video(video_array):

    fig = plt.figure()
    viewer = fig.add_subplot(111)
    plt.ion() # Turns interactive mode on (probably unnecessary)
    fig.show() # Initially shows the figure

    for i in range(video_array.shape[0]):
        viewer.clear()
        viewer.imshow(video_array[i])
        plt.pause(.1)
        fig.canvas.draw()