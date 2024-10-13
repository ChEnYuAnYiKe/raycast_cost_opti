# coding=utf-8

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib as mpl

class Draw_MPC_point_stabilization_v1(object):
    def __init__(self, robot_states: list, init_state: np.array, target_state: np.array, rob_diam=0.3,
                 export_fig=False):
        self.robot_states = robot_states
        self.init_state = init_state
        self.target_state = target_state
        self.rob_radius = rob_diam / 2.0
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-0.8, 3), ylim=(-0.8, 3.))
        # self.fig.set_dpi(400)
        self.fig.set_size_inches(7, 6.5)
        # init for plot
        self.animation_init()

        self.ani = animation.FuncAnimation(self.fig, self.animation_loop, range(len(self.robot_states)),
                                           init_func=self.animation_init, interval=100, repeat=False)

        plt.grid('--')
        if export_fig:
            self.ani.save('./v1.gif', writer='imagemagick', fps=100)
        plt.show()

    def animation_init(self):
        # plot target state
        self.target_circle = plt.Circle(self.target_state[:2], self.rob_radius, color='b', fill=False)
        self.ax.add_artist(self.target_circle)
        self.target_arr = mpatches.Arrow(self.target_state[0], self.target_state[1],
                                         self.rob_radius * np.cos(self.target_state[2]),
                                         self.rob_radius * np.sin(self.target_state[2]), width=0.2)
        self.ax.add_patch(self.target_arr)
        self.robot_body = plt.Circle(self.init_state[:2], self.rob_radius, color='r', fill=False)
        self.ax.add_artist(self.robot_body)
        self.robot_arr = mpatches.Arrow(self.init_state[0], self.init_state[1],
                                        self.rob_radius * np.cos(self.init_state[2]),
                                        self.rob_radius * np.sin(self.init_state[2]), width=0.2, color='r')
        self.ax.add_patch(self.robot_arr)
        return self.target_circle, self.target_arr, self.robot_body, self.robot_arr

    def animation_loop(self, indx):
        position = self.robot_states[indx][:2]
        orientation = self.robot_states[indx][2]
        self.robot_body.center = position
        # self.ax.add_artist(self.robot_body)
        self.robot_arr.remove()
        self.robot_arr = mpatches.Arrow(position[0], position[1], self.rob_radius * np.cos(orientation),
                                        self.rob_radius * np.sin(orientation), width=0.2, color='r')
        self.ax.add_patch(self.robot_arr)
        return self.robot_arr, self.robot_body


class Draw_MPC_point_stabilization_v2(object):
    def __init__(self, robot_states: list, control_states: list, init_state: np.array, target_state: np.array, rob_diam=0.3, export_fig=False):
        self.robot_states = robot_states
        self.init_state = init_state
        self.target_state = target_state
        self.rob_radius = rob_diam / 2.0
        self.control_states = control_states

        # 创建五个子图
        self.fig, axes = plt.subplots(2, 3, figsize=(10, 15))
        self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6 = axes.flatten()
        
        self.ax1.set_xlim(-0.8, 3)
        self.ax1.set_ylim(-0.8, 3)

        # 设置折线图的范围
        self.ax2.set_xlim(0, len(self.robot_states))
        self.ax2.set_ylim(min([s[0] for s in self.robot_states]), max([s[0] for s in self.robot_states]))
        self.ax3.set_xlim(0, len(self.robot_states))
        self.ax3.set_ylim(min([s[1] for s in self.robot_states]), max([s[1] for s in self.robot_states]))
        self.ax4.set_xlim(0, len(self.robot_states))
        self.ax4.set_ylim(min([s[2] for s in self.robot_states]), max([s[2] for s in self.robot_states]))
        self.ax5.set_xlim(0, len(self.control_states))
        self.ax5.set_ylim(min([s[0] for s in self.control_states]), max([s[0] for s in self.control_states]))
        self.ax6.set_xlim(0, len(self.control_states))
        self.ax6.set_ylim(min([s[1] for s in self.control_states]), max([s[1] for s in self.control_states])) 

        # 初始化动画
        self.animation_init()

        # 创建动画
        self.ani = animation.FuncAnimation(self.fig, self.animation_loop, frames=max(len(self.robot_states), len(self.control_states)),
                                           init_func=self.animation_init, interval=100, repeat=False)

        plt.grid('--')
        if export_fig:
            self.ani.save('./v1.gif', writer='imagemagick', fps=100)
        plt.show()

    def animation_init(self):
        # 目标位置的图示
        self.target_circle = plt.Circle(self.target_state[:2], self.rob_radius, color='b', fill=False)
        self.ax1.add_artist(self.target_circle)
        self.target_arr = mpatches.Arrow(self.target_state[0], self.target_state[1],
                                         self.rob_radius * np.cos(self.target_state[2]),
                                         self.rob_radius * np.sin(self.target_state[2]), width=0.2)
        self.ax1.add_patch(self.target_arr)

        # 机器人初始位置的图示
        self.robot_body = plt.Circle(self.init_state[:2], self.rob_radius, color='r', fill=False)
        self.ax1.add_artist(self.robot_body)
        self.robot_arr = mpatches.Arrow(self.init_state[0], self.init_state[1],
                                        self.rob_radius * np.cos(self.init_state[2]),
                                        self.rob_radius * np.sin(self.init_state[2]), width=0.2, color='r')
        self.ax1.add_patch(self.robot_arr)

        # 初始化折线图的线条
        self.line2, = self.ax2.plot([], [], 'r-', lw=2, label="State 0")
        self.line3, = self.ax3.plot([], [], 'g-', lw=2, label="State 1")
        self.line4, = self.ax4.plot([], [], 'b-', lw=2, label="State 2")
        self.line5, = self.ax5.plot([], [], 'r-', lw=2, label="Control 0")
        self.line6, = self.ax6.plot([], [], 'g-', lw=2, label="Control 1")
        
        self.x_data, self.y_data1, self.y_data2, self.y_data3, self.y_data4, self.y_data5 = [], [], [], [], [], []  # 存储折线图的数据

        return self.target_circle, self.target_arr, self.robot_body, self.robot_arr, self.line2, self.line3, self.line4, self.line5, self.line6

    def animation_loop(self, indx):
        # 更新机器人位置
        position = self.robot_states[indx][:2]
        orientation = self.robot_states[indx][2]
        self.robot_body.center = position
        self.robot_arr.remove()  # 移除旧的箭头
        self.robot_arr = mpatches.Arrow(position[0], position[1], self.rob_radius * np.cos(orientation),
                                        self.rob_radius * np.sin(orientation), width=0.2, color='r')
        self.ax1.add_patch(self.robot_arr)

        # 更新折线图数据
        self.x_data.append(indx)
        self.y_data1.append(self.robot_states[indx][0])  # 第一个变量
        self.y_data2.append(self.robot_states[indx][1])  # 第二个变量
        self.y_data3.append(self.robot_states[indx][2])  # 第三个变量
        self.y_data4.append(self.control_states[indx][0])
        self.y_data5.append(self.control_states[indx][1])

        # 更新折线图
        self.line2.set_data(self.x_data, self.y_data1)
        self.line3.set_data(self.x_data, self.y_data2)
        self.line4.set_data(self.x_data, self.y_data3)
        self.line5.set_data(self.x_data, self.y_data4)
        self.line6.set_data(self.x_data, self.y_data5)
    
        return self.robot_arr, self.robot_body, self.line2, self.line3, self.line4, self.line5, self.line6

class Draw_MPC_Obstacle(object):
    def __init__(self, robot_states: list, init_state: np.array, target_state: np.array, obstacle: np.array,
                 rob_diam=0.3, export_fig=False):
        self.robot_states = robot_states
        self.init_state = init_state
        self.target_state = target_state
        self.rob_radius = rob_diam / 2.0
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-0.8, 3), ylim=(-0.8, 3.))
        if obstacle is not None:
            self.obstacle = obstacle
        else:
            print('no obstacle given, break')
        self.fig.set_size_inches(7, 6.5)
        # init for plot
        self.animation_init()

        self.ani = animation.FuncAnimation(self.fig, self.animation_loop, range(len(self.robot_states)),
                                           init_func=self.animation_init, interval=100, repeat=False)

        plt.grid('--')
        if export_fig:
            self.ani.save('obstacle.gif', writer='imagemagick', fps=100)
        plt.show()

    def animation_init(self):
        # plot target state
        self.target_circle = plt.Circle(self.target_state[:2], self.rob_radius, color='b', fill=False)
        self.ax.add_artist(self.target_circle)
        self.target_arr = mpatches.Arrow(self.target_state[0], self.target_state[1],
                                         self.rob_radius * np.cos(self.target_state[2]),
                                         self.rob_radius * np.sin(self.target_state[2]), width=0.2)
        self.ax.add_patch(self.target_arr)
        self.robot_body = plt.Circle(self.init_state[:2], self.rob_radius, color='r', fill=False)
        self.ax.add_artist(self.robot_body)
        self.robot_arr = mpatches.Arrow(self.init_state[0], self.init_state[1],
                                        self.rob_radius * np.cos(self.init_state[2]),
                                        self.rob_radius * np.sin(self.init_state[2]), width=0.2, color='r')
        self.ax.add_patch(self.robot_arr)
        self.obstacle_circle = plt.Circle(self.obstacle[:2], self.obstacle[2], color='g', fill=True)
        self.ax.add_artist(self.obstacle_circle)
        return self.target_circle, self.target_arr, self.robot_body, self.robot_arr, self.obstacle_circle

    def animation_loop(self, indx):
        position = self.robot_states[indx][:2]
        orientation = self.robot_states[indx][2]
        self.robot_body.center = position
        self.robot_arr.remove()
        self.robot_arr = mpatches.Arrow(position[0], position[1], self.rob_radius * np.cos(orientation),
                                        self.rob_radius * np.sin(orientation), width=0.2, color='r')
        self.ax.add_patch(self.robot_arr)
        return self.robot_arr, self.robot_body


class Draw_MPC_tracking(object):
    def __init__(self, robot_states: list, init_state: np.array, rob_diam=0.3, export_fig=False):
        self.init_state = init_state
        self.robot_states = robot_states
        self.rob_radius = rob_diam
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-1.0, 16), ylim=(-0.5, 1.5))
        # self.fig.set_size_inches(7, 6.5)
        # init for plot
        self.animation_init()

        self.ani = animation.FuncAnimation(self.fig, self.animation_loop, range(len(self.robot_states)),
                                           init_func=self.animation_init, interval=100, repeat=False)

        plt.grid('--')
        if export_fig:
            self.ani.save('tracking.gif', writer='imagemagick', fps=100)
        plt.show()

    def animation_init(self, ):
        # draw target line
        self.target_line = plt.plot([0, 12], [1, 1], '-r')
        # draw the initial position of the robot
        self.init_robot_position = plt.Circle(self.init_state[:2], self.rob_radius, color='r', fill=False)
        self.ax.add_artist(self.init_robot_position)
        self.robot_body = plt.Circle(self.init_state[:2], self.rob_radius, color='r', fill=False)
        self.ax.add_artist(self.robot_body)
        self.robot_arr = mpatches.Arrow(self.init_state[0], self.init_state[1],
                                        self.rob_radius * np.cos(self.init_state[2]),
                                        self.rob_radius * np.sin(self.init_state[2]), width=0.2, color='r')
        self.ax.add_patch(self.robot_arr)
        return self.target_line, self.init_robot_position, self.robot_body, self.robot_arr

    def animation_loop(self, indx):
        position = self.robot_states[indx][:2]
        orientation = self.robot_states[indx][2]
        self.robot_body.center = position
        self.robot_arr.remove()
        self.robot_arr = mpatches.Arrow(position[0], position[1], self.rob_radius * np.cos(orientation),
                                        self.rob_radius * np.sin(orientation), width=0.2, color='r')
        self.ax.add_patch(self.robot_arr)
        return self.robot_arr, self.robot_body


class Draw_FolkLift(object):
    def __init__(self, robot_states: list, initial_state: np.array, export_fig=False):
        self.init_state = initial_state
        self.robot_state_list = robot_states
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-1.0, 8.0), ylim=(-0.5, 8.0))

        self.animation_init()

        self.ani = animation.FuncAnimation(self.fig, self.animation_loop, range(len(self.robot_state_list)),
                                                   init_func=self.animation_init, interval=100, repeat=False)
        if export_fig:
            pass
        plt.show()

    def animation_init(self, ):
        x_, y_, angle_ = self.init_state[:3]
        tr = mpl.transforms.Affine2D().rotate_deg_around(x_, y_, angle_)
        t = tr + self.ax.transData
        self.robot_arr = mpatches.Rectangle((x_ - 0.12, y_ - 0.08),
                                             0.24,
                                             0.16,
                                             transform=t,
                                             color='b',
                                             alpha=0.8,
                                             label='DIANA')
        self.ax.add_patch(self.robot_arr)
        return self.robot_arr

    def animation_loop(self, indx):
        x_, y_, angle_ = self.robot_state_list[indx][:3]
        angle_ = angle_ * 180 / np.pi
        tr = mpl.transforms.Affine2D().rotate_deg_around(x_, y_, angle_)
        t = tr + self.ax.transData
        self.robot_arr.remove()
        self.robot_arr = mpatches.Rectangle((x_ - 0.12, y_ - 0.08),
                                             0.24,
                                             0.16,
                                             transform=t,
                                             color='b',
                                             alpha=0.8,
                                             label='DIANA')
        self.ax.add_patch(self.robot_arr)
        return self.robot_arr
