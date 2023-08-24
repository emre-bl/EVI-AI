import cv2
print(1)
# RTSP stream URL
rtsp_url = "http://10.3.128.74:5554/playlist.m3u"
print(2)
# Create VideoCapture object
cap = cv2.VideoCapture(rtsp_url)
print(3)
# Check if the stream is opened successfully
if not cap.isOpened():
	print("Failed to open RTSP stream.")
	exit()
print(4)
# Read and display frames
while True:
	print(".", end="")
	ret, frame = cap.read()
	if not ret:
		break

	# Display the frame
	cv2.imshow("RTSP Stream", frame)
	if cv2.waitKey(1) == ord("q"):
		break

# Release the VideoCapture object and close windows
print(5)
cap.release()
cv2.destroyAllWindows()
print(6)
