import vrep
import time

vrep.simxFinish(-1)  # just in case, close all opened connections
clientID = vrep.simxStart(  # clientID,经测试从0计数，若超时返回-1。若不返回-1，则应该在程序最后调用 simxFinish
    '127.0.0.1',  # 服务端（server）的IP地址，本机为127.0.0.1
    19997,  # 端口号
    True,  # True:程序等待服务端开启（或连接超时）
    True,  # True:连接丢失时，通信线程不会尝试第二次连接
    2000,  # 正：超时时间(ms)（此时阻塞函数时间为5s）负：阻塞函数时间(ms)（此时连接等待时间为5s）！不太理解！
    5)  # 数据传输间隔，越小越快，默认5 # Connect to V-REP

print('Connected to remote API server')

vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

RC1, UR5_joint1_Handle = vrep.simxGetObjectHandle(clientID, 'UR5_joint1', vrep.simx_opmode_blocking)
RC2, UR5_joint2_Handle = vrep.simxGetObjectHandle(clientID, 'UR5_joint2', vrep.simx_opmode_blocking)
RC3, UR5_joint3_Handle = vrep.simxGetObjectHandle(clientID, 'UR5_joint3', vrep.simx_opmode_blocking)
RC4, UR5_joint4_Handle = vrep.simxGetObjectHandle(clientID, 'UR5_joint4', vrep.simx_opmode_blocking)
RC5, UR5_joint5_Handle = vrep.simxGetObjectHandle(clientID, 'UR5_joint5', vrep.simx_opmode_blocking)
RC6, UR5_joint6_Handle = vrep.simxGetObjectHandle(clientID, 'UR5_joint6', vrep.simx_opmode_blocking)

vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_streaming)
vrep.simxGetJointPosition(clientID, UR5_joint2_Handle, vrep.simx_opmode_streaming)
vrep.simxGetJointPosition(clientID, UR5_joint3_Handle, vrep.simx_opmode_streaming)
vrep.simxGetJointPosition(clientID, UR5_joint4_Handle, vrep.simx_opmode_streaming)
vrep.simxGetJointPosition(clientID, UR5_joint5_Handle, vrep.simx_opmode_streaming)
vrep.simxGetJointPosition(clientID, UR5_joint6_Handle, vrep.simx_opmode_streaming)

while True:
    if (vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_buffer)[0]  # 判断vrep是否开始回传数据
        & vrep.simxGetJointPosition(clientID, UR5_joint2_Handle, vrep.simx_opmode_buffer)[
            0]  # [0]是指return中的第0位，也即return code
        & vrep.simxGetJointPosition(clientID, UR5_joint2_Handle, vrep.simx_opmode_buffer)[0]
        & vrep.simxGetJointPosition(clientID, UR5_joint2_Handle, vrep.simx_opmode_buffer)[0]
        & vrep.simxGetJointPosition(clientID, UR5_joint2_Handle, vrep.simx_opmode_buffer)[0]
        & vrep.simxGetJointPosition(clientID, UR5_joint2_Handle, vrep.simx_opmode_buffer)[0]) == vrep.simx_return_ok:
        for i in range(3):  # 提取3次关节角度
            rc1, j1_pos = vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_buffer)
            rc2, j2_pos = vrep.simxGetJointPosition(clientID, UR5_joint2_Handle, vrep.simx_opmode_buffer)
            rc3, j3_pos = vrep.simxGetJointPosition(clientID, UR5_joint3_Handle, vrep.simx_opmode_buffer)
            rc4, j4_pos = vrep.simxGetJointPosition(clientID, UR5_joint4_Handle, vrep.simx_opmode_buffer)
            rc5, j5_pos = vrep.simxGetJointPosition(clientID, UR5_joint5_Handle, vrep.simx_opmode_buffer)
            rc6, j6_pos = vrep.simxGetJointPosition(clientID, UR5_joint6_Handle, vrep.simx_opmode_buffer)

            print("j1_pos:", j1_pos)
            print("j2_pos:", j2_pos)
            print("j3_pos:", j3_pos)
            print("j4_pos:", j4_pos)
            print("j5_pos:", j5_pos)
            print("j6_pos:", j6_pos)
            print("-----------------------")
            time.sleep(0.2)
        break
    else:
        print("waiting for server response...")
        time.sleep(0.5)  # 0.001是我手调出来的，便于演示而已

# 测试服务端是否继续在发送数据给客户端，以第一个关节为例
time.sleep(3)
if vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_buffer)[0] == vrep.simx_return_ok:
    print("客户端待机3秒后，服务端依然在发送数据。")
    print("关节1的角度为", vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_buffer)[1])

elif vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_buffer)[
    0] == vrep.simx_return_novalue_flag:
    print("客户端待机3秒后，服务端已停止发送数据。")

# 强制擦除存放在服务端的指令，再测试服务端是否还在发送数据
print('擦除存放在服务端的指令...')
while True:
    # 因为客户端到服务端的指令是有延迟的，所以需要这个While循环来确保确实已经擦除服务端的命令，实际使用时不必这样测试。
    # 另外这里面的逻辑需要注意一下，第一次检测到vrep.simx_return_novalue_flag时，应该是While循环第一个指令造成的，而不是
    # 当前的那个
    rc1, j1_pos = vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_discontinue)
    if rc1 == vrep.simx_return_ok:
        print("waiting for server response...")
        time.sleep(0.001)  # 0.001是我手调出来的，便于演示而已
    elif rc1 == vrep.simx_return_novalue_flag:
        print("server responds!")
        break

if vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_buffer)[0] == vrep.simx_return_ok:
    print("强制擦除后，服务端依然在发送数据。")
    print("关节1的角度为", vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_buffer)[1])
elif vrep.simxGetJointPosition(clientID, UR5_joint1_Handle, vrep.simx_opmode_buffer)[
    0] == vrep.simx_return_novalue_flag:
    print("强制擦除后，服务端已停止发送数据。")
