import sys
import cv2
import os
from datetime import datetime
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient  # Import BlobServiceClient for Azure Blob Storage

# Azure Face API Configuration
FACE_API_KEY = "<AZURE_FACE_API_KEY>"
FACE_API_ENDPOINT = "<AZURE_FACE_API_ENDPOINT>"

# Azure Blob Storage Configuration
CONNECTION_STRING = "<BLOB_STORAGE_CONNECTION_STRING>"
BLOB_CONTAINER_NAME = "<BLOB_CONTAINER_NAME>"

face_client = FaceClient(FACE_API_ENDPOINT, CognitiveServicesCredentials(FACE_API_KEY))
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

location = "AB1_3"
# Known faces and person group
known_faces = {"Surya": "Surya.png"}
person_group_id = "my_test"

def add_person_to_group(person_group_id, person_name, image_path):
    try:
        # Check if the person group exists
        face_client.person_group.get(person_group_id)
    except Exception:
        # Create the group if it doesn't exist
        face_client.person_group.create(person_group_id=person_group_id, name="Test Group")



    person = face_client.person_group_person.create(person_group_id, person_name)
    with open(image_path, 'rb') as img_file:
        face_client.person_group_person.add_face_from_stream(person_group_id, person.person_id, img_file)
    face_client.person_group.train(person_group_id)

def recognize_faces_live(face_client, frame, person_group_id, threshold=0.5):
    frame_path = "temp_frame.jpg"
    cv2.imwrite(frame_path, frame)

    with open(frame_path, 'rb') as img_file:
        detected_faces = face_client.face.detect_with_stream(img_file)

    if not detected_faces:
        return []

    face_ids = [face.face_id for face in detected_faces]
    results = face_client.face.identify(face_ids, person_group_id=person_group_id)
    recognized_faces = []
    for result in results:
        if result.candidates:
            person_id = result.candidates[0].person_id
            confidence = result.candidates[0].confidence
            if confidence >= threshold:
                person = face_client.person_group_person.get(person_group_id, person_id)
                recognized_faces.append((person.name, confidence))
            else:
                recognized_faces.append(('Not Recognized', confidence))
        else:
            recognized_faces.append(('Not Recognized', 0))
    return recognized_faces

# Add known faces to the person group
for name, image_path in known_faces.items():
    add_person_to_group(person_group_id, name, image_path)

class IntruderDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intruder Detection System")
        self.setGeometry(100, 100, 1200, 800)  # Enlarged window size
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")  # Changed background color

        # Video capture
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Unable to access the camera")

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Title label with professional font
        title_font = QFont("Arial", 24, QFont.Bold)
        self.title_label = QLabel("Intruder Detection System")
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Spacer to center the video display
        self.layout.addStretch()

        # Video display
        self.video_label = QLabel("Initializing...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("border: 2px solid #4CAF50; border-radius: 10px;")
        self.layout.addWidget(self.video_label)

        # Spacer to center the video display
        self.layout.addStretch()

        # Start/Stop button
        self.toggle_button = QPushButton("Stop Camera")
        self.toggle_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.toggle_button.clicked.connect(self.toggle_camera)
        self.layout.addWidget(self.toggle_button)

        # Timer for real-time video processing
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Approx. 30 FPS

        self.running = True  # To manage the camera state
        self.unknown_face_count = 0  # Counter for unknown faces
        
    def update_frame(self):
        """Process video frames and update the GUI."""
        ret, frame = self.cap.read()
        if not ret:
            return

        # Recognize faces
        recognized_faces = recognize_faces_live(face_client, frame, person_group_id)

        # Overlay results on the frame
        for face, confidence in recognized_faces:
            cv2.putText(frame, f"{face} ({confidence:.2f})", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if face == 'Not Recognized':
                # Save the frame as an image
                self.unknown_face_count += 1
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unknown_face_dir = "unknown_faces"
                os.makedirs(unknown_face_dir, exist_ok=True)
                file_path = os.path.join(unknown_face_dir, f"{location}_{timestamp}.png")
                cv2.imwrite(file_path, frame)

                # Upload to blob storage
                self.upload_to_blob(file_path, f"{location}_{timestamp}.png")

        # Convert frame to QImage for PyQt display
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_frame.shape
        bytes_per_line = channels * width
        qt_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def upload_to_blob(self, file_path, file_name):
        """Uploads a file to Azure Blob Storage."""
        try:
            blob_client = container_client.get_blob_client(blob=file_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"Uploaded {file_name} to blob storage.")
        except Exception as e:
            print(f"Error uploading {file_name}: {e}")

    def toggle_camera(self):
        """Start or stop the camera."""
        if self.running:
            self.timer.stop()
            self.cap.release()
            self.video_label.setText("Camera stopped.")
            self.toggle_button.setText("Start Camera")
        else:
            self.cap = cv2.VideoCapture(0)
            self.timer.start(30)
            self.toggle_button.setText("Stop Camera")
        self.running = not self.running

    def closeEvent(self, event):
        """Handle app closure."""
        self.cap.release()
        cv2.destroyAllWindows()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntruderDetectionApp()
    window.show()
    sys.exit(app.exec_())
