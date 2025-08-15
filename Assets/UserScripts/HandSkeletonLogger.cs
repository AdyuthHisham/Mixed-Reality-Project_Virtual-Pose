using System.Collections.Generic;
using UnityEngine;
using Oculus.Interaction.Input;

public class HandSkeletonLogger : MonoBehaviour
{
    public HandSkeletonOVR handSkeletonProvider;
    public Handedness handedness = Handedness.Left;

    private float startTime;
    private float nextLogTime = 0f;
    private float logInterval = 5f;  // 5 second interval

    // Only these joint indices will be logged
    private readonly int[] jointsToLog = { 0, 1, 2, 3, 4 };

    void Start()
    {
        startTime = Time.time;

        Debug.Log($"[HandSkeletonLogger] Logging started for: {handedness}");
        
        int numJoints = handSkeletonProvider[handedness].joints.Length;
        Debug.Log($"[HandSkeletonLogger] Number of joints: {numJoints}");
        Debug.Log("Timestamp,JointIndex,PosX,PosY,PosZ,RotX,RotY,RotZ,RotW");

        nextLogTime = startTime + logInterval;
    }

    void Update()
    {
        if (Time.time >= nextLogTime)
        {
            var skeleton = handSkeletonProvider[handedness];
            if (skeleton == null || skeleton.joints == null)
            {
                Debug.LogWarning("[HandSkeletonLogger] Skeleton data not available.");
                return;
            }

            var timestamp = Time.time - startTime;

            foreach (int i in jointsToLog)
            {
                if (i < 0 || i >= skeleton.joints.Length)
                    continue;

                var joint = skeleton.joints[i];

                Vector3 pos = joint.pose.position;
                Quaternion rot = joint.pose.rotation;

                Debug.Log($"{timestamp:F4},{i},{pos.x:F4},{pos.y:F4},{pos.z:F4},{rot.x:F4},{rot.y:F4},{rot.z:F4},{rot.w:F4}");
            }

            nextLogTime += logInterval;
        }
    }
}
