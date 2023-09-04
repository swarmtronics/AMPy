"""
Module provides the dashboard with evolution of system's parameters
"""
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from celluloid import Camera

def get_dashboard(output_name:str,
                  cart_disp:list,
                  boo:list,
                  stcp:list, 
                  cl_coeff:list,
                  distance:list,
                  angle:list,
                  angle_abs:list,
                  fps:int,
                 ) -> None:
    """
    Creates .gif with simulteneous evolution of the system parameters along with еру original video
    
    :param output_name: name of the output file
    :param cart_disp: cartesian displacement
    :param boo: bond orientational order parameter
    :param stcp: spatio-temporal correlation parameter
    :param cl_coeff: clustering coefficient
    :param distance: mean distance from the center
    :param angle: mean polar angle
    :param angle_abs: absolute value of the mean polar angle
    :param fps: frames per second
    """
    
    fig, ax = plt.subplots()
    fig = plt.figure(layout="constrained", figsize = (12,8))
    
    gs = gridspec.GridSpec(4, 4, figure=fig)
    
    ax1 = fig.add_subplot(gs[:3, :3])
    ax2 = fig.add_subplot(gs[:1, -1])
    ax3 = fig.add_subplot(gs[1:2, -1])
    ax4 = fig.add_subplot(gs[2:3, -1])
    ax5 = fig.add_subplot(gs[3:4, -1])
    ax6 = fig.add_subplot(gs[-1, 0])
    ax7 = fig.add_subplot(gs[-1, 1])
    ax8 = fig.add_subplot(gs[-1, 2])

    camera = Camera(fig)
    
    time = [i for i in range(len(cart_disp))]

    for i in tqdm(range(len(video))):

        ax1.imshow(video[i])
        ax1.text(x = 10, y = 30, s=f'Frame {i}, {round(i/fps, 2)} sec', color ='white')

        ax1.set_title('Source video')

        ax2.set_title('Cartesian displacement')

        ax3.set_title('Bond orientation parameter')

        ax4.set_title('S-t correlation parameter')

        ax5.set_title('Clustering coefficient')

        ax6.set_title('Mean distance from the center')

        ax7.set_title('Mean polar angle')

        ax8.set_title('Mean polar angle path')

        axs = [ax2, ax3, ax4, ax5, ax6, ax7, ax8]
        data = [cart_disp, boo, stcp, cl_coeff, distance, angle, angle_abs]

        for d, ax in zip(data, axs):
            ax.plot(time[0:i], d[0:i], color="blue")
            ax.axis(xmin = min(time), xmax = max(time), ymin = min(d), ymax = max(d) + 
                 (max(d) - min(d))/10)

        camera.snap()


    animation = camera.animate()
    animation.save(output_name)
