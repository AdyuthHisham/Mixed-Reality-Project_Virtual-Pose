using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class UDPReceiver : MonoBehaviour
{
    public int listenPort = 9050;

    private UdpClient udpClient;
    private Thread receiveThread;

    private Quaternion receivedRotation = Quaternion.identity;
    private bool newRotationReceived = false;

    void Start()
    {
        udpClient = new UdpClient(listenPort);
        Debug.Log($"UDP Receiver started on port {listenPort}.");
        // Runs ReceiveData() on a seperate thread to not block the main thread
        receiveThread = new Thread(ReceiveData);
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    void ReceiveData()
    {
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, listenPort);
        while (true)
        {
            try
            {
                byte[] data = udpClient.Receive(ref remoteEndPoint);
                string text = Encoding.UTF8.GetString(data);
                Debug.Log($"Data received from {remoteEndPoint.Address}:{remoteEndPoint.Port} -> {text}");

                // Expecting quaternion as comma-separated string e.g. "x,y,z,w"
                string[] quatParts = text.Split(',');
                if (quatParts.Length == 4)
                {
                    float qx = float.Parse(quatParts[0]);
                    float qy = float.Parse(quatParts[1]);
                    float qz = float.Parse(quatParts[2]);
                    float qw = float.Parse(quatParts[3]);

                    
                    Quaternion quatRotation = new Quaternion(qx, qy, qz, qw);
                    
                    // Reorder axes or flip signs depending on how the IMU is aligned
                    // NEEDS TO BE TESTED MORE
                    receivedRotation = new Quaternion(-quatRotation.y, quatRotation.x, quatRotation.z, quatRotation.w);

                    newRotationReceived = true;
                }
                else
                {
                    Debug.LogWarning("Received data does not have 4 components for quaternion.");
                }
            }
            catch (System.Exception e)
            {
                Debug.LogError("UDP receive error: " + e.Message);
            }
        }
    }

    void Update()
    {
        if (newRotationReceived)
        {
            Debug.Log($"Updating rotation to: {receivedRotation}");
            transform.rotation = receivedRotation;
            newRotationReceived = false;
        }
    }

    void OnApplicationQuit()
    {
        if (receiveThread != null && receiveThread.IsAlive)
        {
            receiveThread.Abort();
            Debug.Log("Receive thread aborted.");
        }
        udpClient.Close();
        Debug.Log("UDP client closed.");
    }
}
