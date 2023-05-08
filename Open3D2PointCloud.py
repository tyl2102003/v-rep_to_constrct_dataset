# -*- coding: utf-8 -*-
import numpy
import open3d as o3d
import cv2
import numpy as np

buffer = cv2.imread('saveImg/rgbImg/rgb.jpg', flags=cv2.IMREAD_UNCHANGED)
color = o3d.geometry.Image(buffer)

buffer1 = cv2.imread('./saveImg/depthImg/depth.png', flags=cv2.IMREAD_UNCHANGED)
depth = o3d.geometry.Image(buffer1)

rgbd = o3d.geometry.RGBDImage()
img = rgbd.create_from_color_and_depth(color, depth, depth_scale=18773)
pd = o3d.geometry.PointCloud()
# camera_intrinsics = [589.4, 589.4, 640.0, 480.0]
camera_intrinsics = o3d.camera.PinholeCameraIntrinsic(640, 480, 589.4, 589.4, 320.0, 240.0)

ex = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])
pcd = pd.create_from_rgbd_image(img, camera_intrinsics, extrinsic=ex)

o3d.visualization.draw([pcd])
o3d.visualization.draw()
# o3d.io.write_point_cloud('tab2.pcd', pcd)
