# DefendX

# DefendX - a Python, OpenCV, Azure Face API, and PyQt-Based Intrusion Detection System 
Project Overview
Intrusion Detection System (IDS) is an advanced security system applied to identify intruders and prevent crimes, particularly against women in universities. The system identifies intruders using Python, OpenCV, Microsoft Azure Face API, and PyQt and sends alerts to security personnel in real time. Integrating facial recognition with Power Automate, it sends quick notifications and response, enhancing campus security.

# Key Features
Facial Recognition-Based Access Control Authorized users' facial data are pre-registered and trained using the Azure Face API. When an individual attempts to enter, the system captures their photo and matches it against the authorized database. Real-Time Unauthorized Person Detection If the face is not matched as an authorized user, the system detects the person as unauthorized. The system captures and logs the photo of the unknown individual. Automated Security Alert System Once the unauthorized face is detected, the image of the photograph is instantly forwarded to the relevant authorities. The image is sent with timestamp via Microsoft Power Automate, and real-time alerts are provided. Easy-to-Use Interface A contemporary GUI developed using PyQt provides an easy-to-use interface for system administrators. Facilitates real-time monitoring of known and unknown faces. Crime Prevention and Campus Safety Primarily deployed to prevent crimes in university campuses, and specifically crimes against women. Serves as an active security measure to deter possible threats from occurring before harm is caused.
 
# Technical Implementation 
1. Data Collection and Training The system starts by collecting facial data from the authorized staff. Images are processed using OpenCV for face detection. Azure Face API is used to train and store face embeddings of authorized staff. 
2. Real-Time Face Detection When a person appears in front of the camera, the system: Captures the face using OpenCV. Directs the captured face to the Azure Face API for identification. If the face is identified as belonging to an authorized person, access is granted. If the face is unknown, it is tagged as unauthorized. 3. Security Alert via Power Automate When an unauthorized individual is identified, the system: Captures a photo of the subject. Directs the image and time stamp to security authorities via Power Automate. Enables authorities to respond promptly to incoming threats.
4. Graphical User Interface (GUI) using PyQt The system uses an interactive PyQt-based dashboard. Displays real-time detection logs and status messages. Offers administrators views of alerts, database update, and configuration setting.

# Technology Stack
Python – Base programming language. OpenCV – Face detection and image processing. 
Microsoft Azure Face API – Cloud-based facial recognition. 
PyQt – GUI development. 
Power Automate – Automates image notifications and alerts. Database – Stores facial data for authenticated users. 
Potential Applications 
University Campuses– Prevents unauthorized access and student safety assurance. 
Corporate Offices – Secures the building by restricting access to authorized personnel. 
Government Buildings – Monitors and prevents unauthorized entry.
Public Transport Security – Identifies potential risks in metro tracks, airports, etc. Smart Homes and Private Properties – Provides home access by facial recognition.

# Future Improvements
Multi-Camera Integration – Enhanced coverage with multiple cameras for different locations.
AI-Based Behavior Analysis – Detection of suspicious behavior through advanced AI models.
Mobile App Integration – Allowing authorities to receive the alert on their mobile app.
Better Database Management – Implementing a more scalable and efficient database solution. Two-Factor Authentication – Combination of facial recognition with another authentication method (e.g., RFID cards, OTPs).
