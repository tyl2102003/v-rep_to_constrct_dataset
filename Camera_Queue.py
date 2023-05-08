import os
import random

import cv2
import vrep
import time
import numpy as np


class Get_RGB_D:
    # camera_rgb_Name = 'kinect_rgb'
    # camera_depth_Name = 'kinect_depth'


    def __init__(self, camera_rgb_name, camera_depth_name):
        self.camera_rgb_Name = camera_rgb_name
        self.camera_depth_Name = camera_depth_name

        self.resolutionX = 640  # Camera resolution: 640*480
        self.resolutionY = 480

        print('Simulation started')
        vrep.simxFinish(-1)  # 关闭潜在的连接
        # 每隔0.2s检测一次, 直到连接上V-rep

        while True:
            # simxStart的参数分别为：服务端IP地址(连接本机用127.0.0.1);端口号;是否等待服务端开启;连接丢失时是否尝试再次连接;超时时间(ms);数据传输间隔(越小越快)
            clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
            if clientID > -1:
                print("Connection success!")
                break
            else:
                time.sleep(0.2)
                print("Failed connecting to remote API server!")
                print("Maybe you forget to run the simulation on v-rep...")

        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)  # 仿真初始化

        _, cameraRGBHandle = vrep.simxGetObjectHandle(clientID, self.camera_rgb_Name, vrep.simx_opmode_blocking)
        _, cameraDepthHandle = vrep.simxGetObjectHandle(clientID, self.camera_depth_Name, vrep.simx_opmode_blocking)
        self.clientID = clientID
        self.cameraRGBHandle = cameraRGBHandle
        self.cameraDepthHandle = cameraDepthHandle

    # get RGB images

    def getImageRGB(self):

        res1, resolution1, image_rgb = vrep.simxGetVisionSensorImage(self.clientID, self.cameraRGBHandle, 0,
                                                                     vrep.simx_opmode_blocking)

        image_rgb_r = [image_rgb[i] for i in range(0, len(image_rgb), 3)]
        image_rgb_r = np.array(image_rgb_r)
        image_rgb_r = image_rgb_r.reshape(self.resolutionY, self.resolutionX)
        image_rgb_r = image_rgb_r.astype(np.uint8)

        image_rgb_g = [image_rgb[i] for i in range(1, len(image_rgb), 3)]
        image_rgb_g = np.array(image_rgb_g)
        image_rgb_g = image_rgb_g.reshape(self.resolutionY, self.resolutionX)
        image_rgb_g = image_rgb_g.astype(np.uint8)

        image_rgb_b = [image_rgb[i] for i in range(2, len(image_rgb), 3)]
        image_rgb_b = np.array(image_rgb_b)
        image_rgb_b = image_rgb_b.reshape(self.resolutionY, self.resolutionX)
        image_rgb_b = image_rgb_b.astype(np.uint8)

        result_rgb = cv2.merge([image_rgb_b, image_rgb_g, image_rgb_r])
        # 镜像翻转, opencv在这里返回的是一张翻转的图
        result_rgb = cv2.flip(result_rgb, 0)
        return result_rgb

        # get depth images

    def getImageDepth(self):
        clientID = self.clientID
        cameraDepthHandle = self.cameraDepthHandle
        resolutionX = self.resolutionX
        resolutionY = self.resolutionY

        res2, resolution2, image_depth = vrep.simxGetVisionSensorDepthBuffer(clientID, cameraDepthHandle,
                                                                             vrep.simx_opmode_blocking)
        result_depth = np.asarray(image_depth)
        result_depth = result_depth * 255 * 255
        result_depth = result_depth.reshape(resolutionY, resolutionX)
        result_depth = result_depth.astype(np.uint16)
        result_depth = cv2.flip(result_depth, 0)
        return result_depth

    def arrayToImage(self, num, tm):
        path = "imgTemp\\" + str(tm) + str(num) + ".jpg"
        if os.path.exists(path):
            os.remove(path)
        ig = self.getImageRGB()
        cv2.imwrite(path, ig)

    # convert array from v-rep to depth image

    def arrayToDepthImage(self, num, tm):

        path = "imgTempDep\\" + str(tm) + str(num) + ".png"
        if os.path.exists(path):
            os.remove(path)
        ig = self.getImageDepth()
        cv2.imwrite(path, ig)


def main():
    list_camera_rgb = ['kinect_rgb#0', 'kinect_rgb#1', 'kinect_rgb#2', 'kinect_rgb#3', 'kinect_rgb#4',
                       'kinect_rgb#5', 'kinect_rgb#6', 'kinect_rgb#7']
    list_camera_depth = ['kinect_depth#0', 'kinect_depth#1', 'kinect_depth#2', 'kinect_depth#3', 'kinect_depth#4',
                         'kinect_depth#5', 'kinect_depth#6', 'kinect_depth#7']

    for num, (rgb, depth) in enumerate(zip(list_camera_rgb, list_camera_depth)):
        rdtime = random.randint(1, 5)
        time.sleep(rdtime)
        tm = str(time.time()).split('.')[0]
        cam = Get_RGB_D(rgb, depth)
        cam.arrayToImage(num, tm)
        cam.arrayToDepthImage(num, tm)


if __name__ == "__main__":
    main()
