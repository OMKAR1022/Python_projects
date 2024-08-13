import cv2
import depthai

# Create a pipeline
pipeline = depthai.Pipeline()

# Define the camera configuration
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setInterleaved(False)
cam_rgb.setFps(30)

# Define the mono camera configuration for depth
mono_left = pipeline.createMonoCamera()
mono_right = pipeline.createMonoCamera()
mono_left.setBoardSocket(depthai.CameraBoardSocket.LEFT)
mono_right.setBoardSocket(depthai.CameraBoardSocket.RIGHT)

# Define stereo depth configuration
stereo = pipeline.createStereoDepth()
stereo.setConfidenceThreshold(200)
stereo.setRectifyEdgeFillColor(0)  # Black, to better see the cutout

# Link the cameras and stereo depth to the output streams
xout_left = pipeline.createXLinkOut()
xout_left.setStreamName("left")

xout_right = pipeline.createXLinkOut()
xout_right.setStreamName("right")

xout_depth = pipeline.createXLinkOut()
xout_depth.setStreamName("depth")

cam_rgb.preview.link(xout_left.input)
mono_left.out.link(stereo.left)
mono_right.out.link(stereo.right)
stereo.disparity.link(xout_depth.input)

# Start the device and pipeline
with depthai.Device(pipeline) as device:
    print("Pipeline started...")
    while True:
        # Get the depth frame
        in_depth = device.getOutputQueue("depth", maxSize=1, blocking=True).get()
        depth_data = in_depth.getData()
        depth_frame = in_depth.getFrame()

        # Convert the depth frame to a grayscale image
        depth_frame_data = depth_frame
        depth_image = (depth_frame / depth_frame.max() * 255).astype('uint8')

        # Display the depth image
        cv2.imshow('Depth Image', depth_image)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
