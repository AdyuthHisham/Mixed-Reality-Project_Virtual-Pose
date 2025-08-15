using System.Collections.Generic;
using UnityEngine;

    public class CustomSkeletonModifier : MonoBehaviour
{
    public struct CustomJointData
{
    public Vector3 Position;
    public Quaternion Rotation;

    public CustomJointData(Vector3 pos, Quaternion rot)
    {
        Position = pos;
        Rotation = rot;
    }
}
    // public OVRSkeleton _skeleton;
    // public ISkeletonDataProvider _dataProvider;

    // Dictionary mapping bone indices (or BoneIds cast to int) to custom joint data
    private Dictionary<int, CustomJointData> jointOverrides = new Dictionary<int, CustomJointData>
    {
        // { 0, new CustomJointData(new Vector3(-0.2094f,0.6862f,0.2895f), new Quaternion(-0.0638f,-0.1855f,-0.5835f,-0.7881f)) }
        // { 2, new CustomJointData(new Vector3(-0.2811f,0.8711f,0.0837f), new Quaternion(0.8231f,-0.2292f,0.3871f,-0.3465f)) }
        // { 2, new CustomJointData(new Vector3(0.7f, 0.8f, 0.9f), new Quaternion(0.0f, 0.7071f, 0.0f, 0.7071f)) }
    };

    public OVRSkeleton.SkeletonPoseData CustomData(OVRSkeleton.SkeletonPoseData rawData)
    {
        OVRSkeleton.SkeletonPoseData customData = rawData; // Copy raw data

        foreach (var kvp in jointOverrides)
        {
            int jointIndex = kvp.Key;
            CustomJointData overrideData = kvp.Value;

            if (jointIndex >= 0 && jointIndex < customData.BoneTranslations.Length)
            {
                customData.BoneTranslations[jointIndex] = new OVRPlugin.Vector3f
                {
                    x = overrideData.Position.x,
                    y = overrideData.Position.y,
                    z = overrideData.Position.z
                };

                customData.BoneRotations[jointIndex] = new OVRPlugin.Quatf
                {
                    x = overrideData.Rotation.x,
                    y = overrideData.Rotation.y,
                    z = overrideData.Rotation.z,
                    w = overrideData.Rotation.w
                };
            }
        }

        customData.IsDataValid = true; // Mark as valid
        Debug.Log("CustomSkeletonModifier:CustomData executed successfully");
        return customData;
    }
}
