#!/usr/bin/env python

from openpose_ros.srv import DetectPeople
from people_msgs.msg import People
import rospy, signal, json

def signal_handler(signal, frame):
     print('\n\033[95mBye!\033[0m')
     print  tcolors.ENDC
     rospy.shutdown()
     sys.exit(0)



class OpenPoseFusion():

    def __init__(self):
        rospy.wait_for_service('/detect_people')
        self.pose_srv = rospy.ServiceProxy('/detect_people', DetectPeople)

        rospy.Subscriber('/clf_detect_dlib_faces_once/people', People, self.people_callback)
        self.pub = rospy.Publisher('detect_people/fusion', String)

        self.people = None
        self.people_processor = PeopleProcessor()


    def run(self):
        while not rospy.is_shutdown():
            people_detection = self.pose_srv()
            print 'got %s people' % (len(res.people_list))
            self.pub.publish(create_json(people_detection))

    def people_callback(people):
        self.people = people

    def create_json(self, person_detection):

        male_count = 0
        female_count = 0

        if self.people is not None:
            if len(self.people) != len(person_detection):
                print 'received data differs!'

            for p in self.people:
                attr = self.people[i].name.split(':')

                if attr[1] == 'male':
                    male_count += 1
                if attr[1] == 'female':
                    female_count += 1

        result = {}

        result['people_detection']['num_people'] = len(res.people_list)
        result['people_detection']['male_count'] = male_count
        result['people_detection']['female_count'] = female_count

        result['people'] = []

        for i, p in enumerate(person_detection):
            people_attribute = {}

            if i < len(self.people):

                attr = self.people[i].name.split(':')

                people_attribute['name'] = attr[0]
                people_attribute['age'] = attr[1]
                people_attribute['gender'] = attr[2]

            people_attribute['pose'] = self.people_processor.getPose(p)
            people_attribute['gesture'] = self.people_processor.getGesture(p)

            result['people'].append(people_attribute)

        return str(json(result))

class PeopleProcessor():

    def getGesture(self, person_detection):
        return 'stantting'

    def getPose(self, person_detection):
        return 'stantting'

if __name__ == "__main__":
    
    # add SIGINT handler for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)

    rospy.init_node('openpose_bridge')

    opf = OpenPoseFusion()

    opf.run()