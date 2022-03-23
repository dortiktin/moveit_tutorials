class MoveGroupPythonIntefaceTutorial(object):
  def __init__(self):
    super(MoveGroupPythonIntefaceTutorial, self).__init__()
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    self.robot = moveit_commander.RobotCommander()
    self.scene = moveit_commander.PlanningSceneInterface()
    self.group_name = "panda_arm"
    self.move_group = moveit_commander.MoveGroupCommander(group_name)
    self.planning_frame = move_group.get_planning_frame()
    self.eef_link = move_group.get_end_effector_link()
    self.box_name = ''

  def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
      attached_objects = self.scene.get_attached_objects([self.box_name])
      is_attached = len(attached_objects.keys()) > 0
      is_known = self.box_name in self.scene.get_known_object_names()
      if (box_is_attached == is_attached) and (box_is_known == is_known):
        return True
      rospy.sleep(0.1)
      seconds = rospy.get_time()
    return False

  def add_box(self, timeout=4):
    box_pose = geometry_msgs.msg.PoseStamped()
    box_pose.header.frame_id = "panda_leftfinger"
    box_pose.pose.orientation.w = 1.0
    box_pose.pose.position.z = 0.07
    self.box_name = "box"
    self.scene.add_box(self.box_name, box_pose, size=(0.1, 0.1, 0.1))
    return self.wait_for_state_update(box_is_known=True, timeout=timeout)

  def attach_box(self, timeout=4):
    grasping_group = 'hand'
    touch_links = self.robot.get_link_names(group=grasping_group)
    self.scene.attach_box(self.eef_link, self.box_name, touch_links=touch_links)
    return self.wait_for_state_update(box_is_attached=True, box_is_known=False, timeout=timeout)

  def detach_box(self, timeout=4):
    self.scene.remove_attached_object(self.eef_link, name=self.box_name)
    return self.wait_for_state_update(box_is_known=True, box_is_attached=False, timeout=timeout)
  
