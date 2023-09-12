import numpy as np


def get_input(Vx, Vy, w):
    # Angles between wheels
    theta1 = 0
    theta2 = 120
    theta3 = 240
    # Distance between robot center to wheel
    radius = 0.2
    # Array containing coefficients of V1 & V2 & V3 after resolving in x-direction & y-direction
    arr = np.array(
        [
            [np.cos((theta1 + 90) * (np.pi / 180)), np.cos((theta2 + 90) * (np.pi / 180)),
             np.cos((theta3 + 90) * (np.pi / 180))],
            [np.sin((theta1 + 90) * (np.pi / 180)), np.sin((theta2 + 90) * (np.pi / 180)),
             np.sin((theta3 + 90) * (np.pi / 180))],
            [1 / radius, 1 / radius, 1 / radius]
        ]
    )
    # Array containing Vx & Vy & w input by user
    velocity = np.array([
        [Vx],
        [Vy],
        [w]
    ])
    # multiplying a 3x3 array (coefficients inverse matrix) & 3x1 array (input by user) to obtain V1, V2, V3
    v1, v2, v3 = np.matmul(np.linalg.pinv(arr), velocity)

    return v1, v2, v3


def get_pwm(v1, v2, v3):
    # Assume Max RPM equal 1500
    pwm_1 = v1[0] * 255/1500
    pwm_2 = v2[0] * 255/1500
    pwm_3 = v3[0] * 255/1500

    return pwm_1, pwm_2, pwm_3


# Prompt user to enter Vx & Vy & W (omega)
V_x = float(input("Enter Vx: "))
V_y = float(input("Enter Vy: "))
W_omega = float(input("Enter W (omega): "))

v1, v2, v3 = get_input(V_x, V_y, W_omega)

pwm_1, pwm_2, pwm_3 = get_pwm(v1, v2, v3)

# printing speed of motors
print("Motor Angular Velocity:")
print(f"V1 = {np.round(v1[0],3)}")
print(f"V2 = {np.round(v2[0],3)}")
print(f"V3 = {np.round(v3[0],3)}")

# Drive Each motor using Cytron driver
print("PWM value driving motor using cytron driver:")

if pwm_1 > 255 or pwm_2 > 255 or pwm_3 > 255:
    print("PWM Driving --> Velocity greater than maximum assumed!!!")
else:
    if pwm_1 < 0:
        print(f"PWM 1 = {abs(int(pwm_1))} Negative Direction")
    else:
        print(f"PWM 1 = {int(pwm_1)}")

    if pwm_2 < 0:
        print(f"PWM 2 = {abs(int(pwm_2))} Negative Direction")
    else:
        print(f"PWM 2 = {int(pwm_2)}")

    if pwm_3 < 0:
        print(f"PWM 3 = {abs(int(pwm_3))} Negative Direction")
    else:
        print(f"PWM 3 = {int(pwm_3)}")
