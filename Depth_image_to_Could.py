import cv2
import numpy as np
# import open3d as o3d

import time


class point_cloud_generator:

    def __init__(self, rgb_file, depth_file, save_txt, camer_in=None):
        if camer_in is None:
            camer_in = [589.4, 589.4, 640.0, 480.0]
        self.rgb_file = rgb_file
        self.depth_file = depth_file
        self.save_txt = save_txt

        self.rgb = cv2.imread(self.rgb_file, cv2.IMREAD_UNCHANGED)
        self.depth = cv2.imread(self.depth_file, cv2.IMREAD_UNCHANGED)

        # print("your depth image shape is:", self.depth.shape)

        self.width = self.depth.shape[1]
        self.height = self.depth.shape[0]

        self.camer_in = camer_in
        self.depth_scale = 18773

    def compute(self):
        t1 = time.time()

        depth = np.asarray(self.depth, dtype=np.uint16).T

        self.Z = depth / self.depth_scale
        fx, fy, cx, cy = self.camer_in

        X = np.zeros((self.width, self.height))
        Y = np.zeros((self.width, self.height))
        for i in range(self.width):
            X[i, :] = np.full(X.shape[1], i)

        self.X = ((X - cx / 2) * self.Z) / fx
        for i in range(self.height):
            Y[:, i] = np.full(Y.shape[0], i)
        self.Y = ((Y - cy / 2) * self.Z) / fy

        data_ply = np.zeros((6, self.width * self.height))
        data_ply[0] = -self.X.T.reshape(-1)
        data_ply[1] = -self.Y.T.reshape(-1)
        data_ply[2] = self.Z.T.reshape(-1)
        img = np.array(self.rgb, dtype=np.uint8)
        data_ply[3] = img[:, :, 0:1].reshape(-1)
        data_ply[4] = img[:, :, 1:2].reshape(-1)
        data_ply[5] = img[:, :, 2:3].reshape(-1)
        self.data_ply = data_ply
        t2 = time.time()
        print('calcualte 3d point cloud Done.', t2 - t1)

    def write_txt(self):
        start = time.time()
        float_formatter = lambda x: "%.4f" % x
        points = []
        for i in self.data_ply.T:
            if i[2] != 3.4637511319448144:
                points.append("{} {} {} {} {} {}\n".format
                              (float_formatter(i[0]), float_formatter(i[1]), float_formatter(i[2]),
                               int(i[5]), int(i[4]), int(i[3])))
        file = open(self.save_txt, 'w')
        file.write("".join(points))
        # file = open(self.save_ply, "w")
        # file.write('''ply
        # format ascii 1.0
        # element vertex %d
        # property float x
        # property float y
        # property float z
        # end_header
        # %s
        # ''' % (len(points), "".join(points)))
        file.close()
        end = time.time()
        print("Write into .txt file Done.", end - start)


if __name__ == '__main__':
    camer_in = [589.4, 589.4, 640.0, 480.0]
    rgb_file = r"C:\Users\21140\PycharmProjects\v-repAPI\imgTemp\frame.jpg"
    depth_file = r"C:\Users\21140\PycharmProjects\v-repAPI\imgTempDep\frame.png"
    save_txt = "creo_demo.txt"
    a = point_cloud_generator(
        rgb_file=rgb_file,
        depth_file=depth_file,
        save_txt=save_txt,
        camer_in=camer_in
    )
    a.compute()
    a.write_txt()
