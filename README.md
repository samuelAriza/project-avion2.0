# Challenge

Implement an air traffic control system.

### Description

It is required to implement an air traffic control system to manage the takeoff and landing of airplanes at an airport.

------------


### Solution
In the first instance 11 .json files are created, these files are created in order to support the understanding of how the simulation works as the data is randomly generated. Two of the files store the randomly generated dummy data; one file for departure aircraft and one for arrival aircraft; data_exit.json and data_entry.json respectively. Eight .json files that store the data of the 8 queues created according to each priority level and type: outbound or inbound. In addition, a queues.json file containing the information of the queues, which serves as a support to visualize the queues in an easier way.

Two tracks are created, a starting track and a finishing track. Both are initially free.

The eight queues corresponding to each type and priority are created. Initially the queues are empty. Subsequently, the glue method of the queue_priority class has as parameter an item that is a .json file, this method takes the data from that file and organizes them according to the time, resulting in the first of each queue being the least compared according to the time, that is, the next aircraft to depart.

What the order function does is that it receives each file and omits the cancelled planes, so that the queues have only the planes that are not cancelled, so that when the queueing method is used, the planes that are already cancelled are not counted.

Before starting the simulation, an aircraft is allowed to enter.

The order function described above is called and queued respectively.

The firsts function takes the first of each queue to organize them according to time, resolves by priority in case of any time tie, resolves according to priority; 1. Emergency, 2.Special, 3. Performs penalization of departing aircraft that are late. It receives as parameters: value, value_1, value_2, value_3 and type. These parameters refer to the 4 queues of the type type which can be exit or entry.

The assign_track function manages the tracks and internally calls the first function described above.

#### The following versions are used for this purpose:
- Python 3.10.6

------------

Developed by Samuel Ariza, EAFIT University student.