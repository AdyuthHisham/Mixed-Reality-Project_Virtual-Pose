## Links and stuff
1. [Drive folder](https://chalmersindustriteknik-my.sharepoint.com/personal/morten_kristoffersen_chalmersindustriteknik_se/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fmorten%5Fkristoffersen%5Fchalmersindustriteknik%5Fse%2FDocuments%2FDocuments%2FMSc%2FAdyuth&ga=1)
# Week 27
- Lit Survey: Most of the people using these VR headsets use the controller and do some coding black magic to simulate a hand or something by flipping it and attaching it to the stump. Must be super easy ig.
- QR based approach might work - I mean I believe the EMG sensor would be at the stump. That can be hard coded to be the end point of the wrist or something.
- [[Lit Survey#^af2ee5]] Looks like an interesting approach. My idea is the generate a basic skeleton and using this detection system try matching the upper limb to the skeleton as much as I can and from there do the tracking or something. Will need RGB camera data from headset. Apparently pass through cameras are something I can yoink. Should probably check that out. [Check this out to try the passthrough camera](https://skarredghost.com/2025/03/17/how-to-camera-access-meta-quest-3-unity-6/) 
	- Small problem, the paper works on identifying the individual using their lower limbs and **face**. No face when you're wearing the headset. 
- Samples are working - PassthroughCameraApiSamples
- [Meta Quest Tutorial - Im using this as my base](https://youtu.be/2gSVPW8L6ps?feature=shared)
- **CANT FIND VIRTUAL HANDS**
- I doubt I can implement marker tracking or limb tracking if this is the data I have ![[oculus_cast_video_07_04_2025_13_33_07.mp4]]
# Week 28
- Screwing around with Full Body Tracking
- Does full body tracking work without hands?
- Can I use myoband data and fuse it with existing body tracking data to make a full body tracking method
	- In what way should I fuse it, as in the myoband data should be in what format
- HandSkeletonOVR is the top most level where the hand tracking data is obtained (ig)
	- My sensor data can be injected but it needs to follow the HandSkeleton joint structure
- Tested body tracking with right forearm covered by black cloth
	- Janky but shoulder and upper arm movement looks decent
	- Number of joints: 26
	- OVRPlugin.BoneId has enums for hand ids
- Check out human targeter - update skeleton
- ![[nnsrlV5N0fg2tMU_0C-v3OzEXmtmY_ni34AGuKFU1II.webp]] BoneID Meta Quest
 
- ![[Figure_1.png]] Rough Box plot for shits and giggles of Log data
# Week 29
* [Struct containing the Bone Pos + Rot](https://developers.meta.com/horizon/reference/unity/v72/struct_o_v_r_skeleton_skeleton_pose_data)
* ~~Apparently position doesnt matter for hand bone. Since the joint length and everything is already known only the position of the root matters (ig)~~ Only for Oculus
* I am using OpenXR which cares about Pos and Rot
* Coord systems
	* ![[unity-axis-with-rotation.png]] Unity Coord system
	* ![[Pasted image 20250714131401.png]]OpenXR Coord system
* Wrote some code for CustomOVRSkeleton
	* I have no idea how to implement it
	* Ig the armatures are overwriting it
	* Might need to simplify the scenario and just show hands or somethign
* Mooching off sample scene
	* Not shwoing, only displaying the previous scene I had generated
* Set Bone Pose of Left hand to zero
	* Shit was rigid and stagnant
	* All I am doing is changing how it shows on unity
		* The gestures still track the original hand pose estimation
* I just need to control hand root position
* Check out debugger - Unity + VS
* Need to check out MeshRenderer
* Put a breakpoint in MEshRendered and use Unity debugger to figure out what happens
# Week 30
* Root pose can be manipulated now
	* But need to manipulate it so that it adds on to the original value
	* To simulate a longer or shorter limb 
	* Jack shit - Not being manipulated
		* When adding orientation it moves around but Idk what exactly that is
		* RootPose resetting maybe?
* RootPose manipulation is working but idk how
	* I mean how does position and quats influence it, I dont understand 
	* Also I set a hard coded value but the whole thing is still moving 
# Week 31
* Fourier transform the IMU values and remove the noise	
* Just read Quat from the sensor using ```Read_and_plot.py```
# Week 32
* Data being sent from PC to Quest using ```UDPReceiver``` and ```UDPSender```.
	* This is over the internet; apparently it is possible to send directly using ADB but need to experiment and find out. I think RPI Zero would work. BUT that means porting the libemg to Linux.
* Data from armband is being sent over to meta quest using UDP.
	* ~~Coordinate axes are different for sensor and unity so I have to fix that~~
		* Maybe somewhat sometimes working
	* Need to add sensor on a stick system
		* I.e. simulate how the sensor would work when connected to the limb and visualizing the hand
	* And then attach to OVRSkeleton
* [Paper has interesting references](https://www.webofscience.com/wos/woscc/full-record/WOS:000722226300027)
	* The papers are focused on Gait. If hand movements can be classified it'll be seski
	* [For gait, there are stance and swing states. When acceleration is zero it is a stance state. - Zero crossing - time hueristics](https://ieeexplore.ieee.org/document/4209463)
	* [Goes more in depth when compared to above paper - has algorithms](https://ieeexplore.ieee.org/document/5286542)
* Im trying to convert quats from local to global
	* Kinda not working cuz my quat average calibration method is maybe not working