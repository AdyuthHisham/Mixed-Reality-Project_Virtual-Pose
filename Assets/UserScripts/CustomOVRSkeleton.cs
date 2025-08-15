using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;



/// <summary>
/// Custom skeleton class that extends OVRSkeleton behavior.
/// Allows modification or override of skeleton pose data.
/// </summary>
public class CustomSkeleton : OVRSkeleton
{
    private IOVRSkeletonDataProvider customDataProvider;
    protected override void Start()
    {
        base.Start(); // Make sure OVRSkeleton's Start() runs

        // Your custom logic
        // GameObject handObj = GameObject.Find("OVRHandPrefabLeft");
        // if (handObj != null)
        // {
        //     customDataProvider = handObj.GetComponent<IOVRSkeletonDataProvider>();
        //     if (customDataProvider != null)
        //     {
        //         Debug.Log("Custom provider assigned from OVRHandPrefabLeft.");
        //     }
        // }
        customDataProvider = GetComponentInParent<IOVRSkeletonDataProvider>(true);
        if (customDataProvider != null && customDataProvider is MonoBehaviour mb)
        {
            Debug.Log($"Custom provider assigned {mb.name}");
        }

    }

    public CustomSkeletonModifier customiser;
    protected override void Update()
    {
        // base.Update();
        if (!IsInitialized || customDataProvider == null)
        {
            Debug.Log("OVRHandPrefabLeft not initialized");
            return; // Avoid updating if not ready
        }

        // Get the raw skeleton pose data from the data provider
        var rawData = customDataProvider.GetSkeletonPoseData();

        // Skeleton Type is: XRHandLeft
        // Debug.Log("Skeleton Type is: " + customDataProvider.GetSkeletonType());
        // if (customDataProvider is OVRHand hand)
        // {
        //     Debug.Log("IsTracked: " + customDataProvider.IsTracked);
        //     Debug.Log("HandConfidence: " + customDataProvider.IsDataHighConfidence);
        //     Debug.Log("TrackingConfidence: " + customDataProvider.HandConfidence);
        // }

        if (rawData.BoneTranslations == null || rawData.BoneTranslations.Length == 0)
        {
            Debug.LogWarning("rawData has no bone translations.");
        }

        if (!rawData.IsDataValid)
        {
            Debug.Log("rawData is NULL");
            return; // Avoid updating if not ready
        }
        if (customDataProvider != null)
        {
            Debug.Log("Using customDataProvider to modify skeleton data.");
        }
        else
        {
            Debug.Log("No customDataProvider available, using rawData as is.");
        }

        // Apply override if available, else use raw data as is
        var data = (customiser != null && customDataProvider != null)
            ? customiser.CustomData(rawData)
            : rawData;

        if (_bones == null || _bones.Count == 0)
        {
            Debug.LogWarning("CustomSkeleton: _bones list is empty or null!");
            return;
        }


        // Loop through each bone and update transforms
        for (int i = 0; i < _bones.Count; i++)
        {
            var boneTransform = _bones[i].Transform;
            if (boneTransform == null)
            {
                Debug.LogWarning($"Bone {i} has null transform.");
                continue;
            }

            // Convert positions and rotations from OpenXR (flipped Z) coordinate space to Unity space
            Vector3 pos = data.BoneTranslations[i].FromFlippedZVector3f();
            Quaternion rot = data.BoneRotations[i].FromFlippedZQuatf();

            // for (int j = 0; j <= 1; j++)
            // {
            //     Vector3 pos_bug = data.BoneTranslations[j].FromFlippedZVector3f();
            //     Quaternion rot_bug = data.BoneRotations[j].FromFlippedZQuatf();

            //     Debug.Log($"Joint {j} - Pos: {pos_bug.x:F4}, {pos_bug.y:F4}, {pos_bug.z:F4} | Rot: {rot_bug.x:F4}, {rot_bug.y:F4}, {rot_bug.z:F4}, {rot_bug.w:F4}");
            // }

            int parentIndex = _bones[i].ParentBoneIndex;
            bool isParentValid = IsValidBone((BoneId)parentIndex);

            Vector3 parentPos = (isParentValid
                ? data.BoneTranslations[parentIndex]
                : data.RootPose.Position).FromFlippedZVector3f();

            Quaternion parentRot = (isParentValid
                ? data.BoneRotations[parentIndex]
                : data.RootPose.Orientation).FromFlippedZQuatf();

            float invScale = data.RootScale > 0f ? 1f / data.RootScale : 1f;
            Quaternion invParentRot = Quaternion.Inverse(parentRot);

            // Calculate local position and rotation relative to parent bone
            Vector3 localPos = invParentRot * (invScale * (pos - parentPos));
            Quaternion localRot = invParentRot * rot;

            // Apply local transform to bone
            boneTransform.localPosition = localPos;
            boneTransform.localRotation = localRot;
        }
    }

}