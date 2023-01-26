# Research Track I - Second Assignment
The assignment consist of a development of a package that interact with a simulation of a simple robot in Gazebo. The package contains three nodes:
- Node A: A node that implements an action client, allowing the user to set a target (x, y) or to cancel it. The node
also publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z), by relying on the values
published on the topic /odom. Please consider that, if you cannot implement everything in the same node, you
can also develop two different nodes, one implementing the user interface and one implementing the publisher
of the custom message. 
- Node B: A service node that, when called, prints the number of goals reached and cancelled.
- Node C: A node that subscribes to the robot’s position and velocity (using the custom message) and prints the
distance of the robot from the target and the robot’s average speed. Use a parameter to set how fast the
node publishes the information. 
- Has also been implemented a **.launch** file that starts the whole simulation and the Noe A. 

*The launch file starts the simulator and the node in the same window so you can not correctly display the request for the location to be reached. Just press enter to have the request printed on the terminal again.*

# Intalling & Run
Clone this project and the simulation repository(https://github.com/CarmineD8/assignment_2_2022) inside a ROS workspace. Before starting anything you have to run the master process of ROS
```bash
  rocore
```
Then to start the simulation run the launch file
```bash
   roslaunch Assignment_2 assignment_2.launch
```
To call process B or C:
```bash
  rosrun Assignment_2 node_b.py
  rosrun Assignment_2 node_c.py
```

***Attention !*** To run correctly the package's node rename the package "Assignment_2"

# How works
- Process A: 
```
Initialize object Pose() and Twist()
global variable pub_info, target_reached, target_canceled, service, pub_target
	
function clbk_odom(CustomMessage: msg){
  get from msg the position and velocity of the robot
  then publish them to the custom message tag for
  robot info
  
	msg_info <- Info()
	
	msg_info.x <- msg.x
	msg_info.y <- msg.y
	msg_info.vel_x <- msg.vx
	msg_info.vel_y <- msg.vy
  
  publish(msg_info)
} 
		
function getCordinatesFromConsole(){
  print(Set a new target)
  
  while True {
    x <- print (x = )
    y <- print (y = )
    if x AND y are a proper numbers Then
      exit from the while
  }
  return x, y
}
	
function ltk_tgt(double: x,double: y){
  target <- Point()
	
	target.x <- x
	target.y <- y	
	target.z <- 0
	
	publish(target)
}
	

function get_info_goal(CustomMessage: req){
  response <- targetResponse(boudle: target_reached,double: target_canceled)
	return response
}	

main(){

	#Initialization of elements
	pose <- PoseStamped()
	double: target_reached <- 0
	double: target_canceled <- 0
	
	init node A
	
  client <- new SimpleActionClient on tag '/reaching_goal' using CustomMessage of assignment_2_2022.msg.PlanningAction

  pub_info <- new publisher on '/bot_info' that use CustomMessage Info
  pub_target <- new publisher on '/tgt' that use CustomMessage Point
	
  sub_odom <- new subscriber of '\odom' with CusmoMessage Odometry
	service <- new service of 'goal_info' with message targetwho that use a callback function = get_info_goal
	
	client.wait_for_server()
		
	while True {
		p <- getCordinatesFromConsole()
		
		ltk_tgt(p[0],p[1])
		pose.x = p[0];
		pose.y = p[1];
		pose.z = 0;
		
		goal <- create a new goal with target_pose = pose
			
		client.send_goal(goal)
				
		finished = False
    
		print(Do you wanna cancel this target ? (Y/N))
    
		while not finished {
      res <- read from commandline
				if res = 'Y' OR res = 'y' OR res = 'yes':
					finished <- True					
					client.cancel_goal()						
			else 				
				time.sleep(1)		
				state <- client.get_state()
				if(state != 1 and state != 0) Then
					print("Targhet reachedd!) 				
					finished <- True 
    		}
			  
		
		time.sleep(1)
		state = client.get_state()
		if(state = 2) Then			
			target_canceled <- target_canceled + 1
		elif(state == 3) Then			
			target_reached <- target_reached + 1
		else
			printf(Error...)
	}
}
'''
