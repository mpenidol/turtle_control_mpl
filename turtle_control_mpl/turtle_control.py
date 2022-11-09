import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
import math
import numpy as np

class Turtle_Control(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        #self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        #self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.get_logger().info("Controller")
        self.init_goal()
        self.init_subscriber()
        self.init_variables()
        self.init_publisher()
        #ros2 topic pub /turtle1/goal geometry_msgs/msg/Pose2D "{x: 7.0, y: 7.0, theta: 0.0}"


    def init_goal(self):
        self.goal_publisher = self.create_publisher(Pose2D, '/turtle1/goal', 10)
        self.timer = self.create_timer(0.5, self.send_goal)
        return

    def send_goal(self):
        msg = Pose2D()
        

        msg.x = 7.0
        msg.y = 7.0
        msg.theta = 0.0
        self.goal_publisher.publish(msg)



    def init_subscriber(self):
        self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.goal_subscriber = self.create_subscription(Pose2D,'/turtle1/goal',self.goal_callback,10)
        return
   
    def pose_callback(self, pose: Pose):
        
        self.posicao_atual_x = pose.x
        self.posicao_atual_y = pose.y
        self.posicao_atual_theta = pose.theta
        #print('X: ', self.posicao_atual_x, 'Y: ', self.posicao_atual_y, 'Theta: ', self.posicao_atual_theta)
                
  
    def goal_callback(self, goal: Pose2D):
        self.goal_x = goal.x
        self.goal_y = goal.y
        self.goal_theta = goal.theta
        
        #print('X: ', self.goal_x, 'Y: ', self.goal_y, 'Theta: ', self.goal_theta)

    def init_variables(self):
        #print('X: ', self.posicao_final_x, 'Y: ', self.posicao_final_y, 'Theta: ', self.posicao_final_theta)
    
        
        #self.x = self.posicao_final_x - self.posicao_atual_x
        #self.y = self.posicao_final_y - self.posicao_atual_y
        
        #self.ro = math.sqrt((self.x)^2+ (self.y)^2)
        #self.alpha = math.atan(self.y/self.x) - self.posicao_atual_theta

        self.v_max = 0.1
        self.k = 0.5

        #self.v_linear = self.v_max*np.tanh(self.ro)
        #self.omega = self.k * self.alpha
        
        return
    
    
    def init_publisher(self):
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.send_cmd_vel)
        return

    def send_cmd_vel(self):
        self.x = self.goal_x - self.posicao_atual_x
        self.y = self.goal_y - self.posicao_atual_y
        print('Erro X: ' ,self.x, 'Erro Y: ', self.y)
        self.ro = math.sqrt((self.x)**2+ (self.y)**2)
        self.alpha = math.atan2(self.y,self.x) - self.posicao_atual_theta
        self.v_linear = self.v_max*np.tanh(self.ro)
        self.omega = self.k * self.alpha
        
        msg = Twist()
        msg.linear.x = self.v_linear
        msg.angular.z = self.omega
        self.cmd_vel_publisher.publish(msg)



def main(args=None):
    #print('Hi from turtle_control_mpl.')
    rclpy.init(args=args)
    node = Turtle_Control()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
