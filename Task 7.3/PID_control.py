# class PID_Controller:
#     def __init__(self, Kp, Ki, Kd, target_position):
#         self.Kp = Kp
#         self.Ki = Ki
        
#         self.Kd = Kd
#         self.target_position = target_position
#         self.integral_error = 0
#         self.previous_error = 0

#     def cal_output(self, current_position, dt):
        
#         error = self.target_position - current_position

#         P = self.Kp * error
#         self.integral_error += error * dt  
        
#         I = self.Ki * self.integral_error # integ. term
#         D = self.Kd * (error - self.previous_error) / dt  #def. term

#         control_output = P + I + D


#         control_output = max(min(control_output, MAX_OUTPUT), MIN_OUTPUT)

#         self.previous_error = error

#         return control_output


# MAX_OUTPUT = 100.0

# MIN_OUTPUT = -100.0

# # Ex
# target_position = 100.0
# controller = PID_Controller(Kp=0.1, Ki=0.01, Kd=0.05, target_position=target_position)

# current_position = 0.0
# sample_time = 0.01  #control loop rate
# for _ in range(100):
#     control_output = controller.cal_output(current_position, sample_time)
import numpy as np

class KinematicModel:
    def __init__(self):
        self.theta1 = 0
        self.theta2 = 120
        self.theta3 = 240
        self.radius = 0.2

        # Co eff matrix for V resalution
        self.arr = np.array([
            [np.cos((self.theta1 + 90) * (np.pi / 180)), np.cos((self.theta2 + 90) * (np.pi / 180)),
             np.cos((self.theta3 + 90) * (np.pi / 180))],
            [np.sin((self.theta1 + 90) * (np.pi / 180)), np.sin((self.theta2 + 90) * (np.pi / 180)),
             np.sin((self.theta3 + 90) * (np.pi / 180))],
            [1 / self.radius, 1 / self.radius, 1 / self.radius]
        ])

    def resolve_velocity(self, Vx, Vy, w):
        velocity = np.array([[Vx], [Vy], [w]])
        v1, v2, v3 = np.matmul(np.linalg.pinv(self.arr), velocity)
        return v1[0], v2[0], v3[0]

    def calculate_pwm(self, v1, v2, v3):
        max_rpm = 1500
        pwm_1 = v1 * 255 / max_rpm
        pwm_2 = v2 * 255 / max_rpm
        
        pwm_3 = v3 * 255 / max_rpm
        return pwm_1, pwm_2, pwm_3

class PID_Controller:
    def __init__(self, Kp, Ki, Kd, target_position):
        self.Kp = Kp
        
        self.Ki = Ki
        
        self.Kd = Kd
        self.target_position = target_position
        self.integral_error = 0
        self.previous_error = 0

    def calculate_output(self, current_position, dt):
        error = self.target_position - current_position

        P = self.Kp * error
        
        self.integral_error += error * dt  
        
        I = self.Ki * self.integral_error# integ. term
        D = self.Kd * (error - self.previous_error) / dt# def. term

        control_output = P + I + D
        control_output = max(min(control_output, MAX_OUTPUT), MIN_OUTPUT)

        self.previous_error = error

        return control_output

MAX_OUTPUT = 100.0
MIN_OUTPUT = -100.0

# Ex
if __name__ == "__main__":
    kinematic_model = KinematicModel()
    Vx = float(input("Enter Vx: "))
    Vy = float(input("Enter Vy: "))
    w = float(input("Enter w (omega): "))

    v1, v2, v3 = kinematic_model.resolve_velocity(Vx, Vy, w)
    pwm_1, pwm_2, pwm_3 = kinematic_model.calculate_pwm(v1, v2, v3)

    print("Motor Angular Velocity:")
    print(f"V1 = {np.round(v1, 3)}")
    print(f"V2 = {np.round(v2, 3)}")
    print(f"V3 = {np.round(v3, 3)}")

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
