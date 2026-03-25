# 🛡️ NileCortex V-SECURE PRO
### AI-Powered Biometric Recognition System

**Developed & Engineered by:** `OSMAN IBRAHIM`  
**System Version:** `1.0.0 (Production Build)`

---

## 📋 Overview
**V-SECURE PRO** is a professional-grade facial recognition and attendance management system. It utilizes advanced deep learning architectures to provide real-time identification, biometric logging, and automated security reporting. The system is designed with a modern, user-friendly interface to bridge the gap between complex AI and practical daily use.

## 🚀 System Architecture & AI Models
* **Face Recognition Engine:** Powered by the **VGG-Face** deep neural network, providing high accuracy in diverse lighting conditions.
* **Detector Backend:** Uses **OpenCV Haar Cascades** for lightning-fast face localization.
* **Core Framework:** Built on **TensorFlow and Keras** for real-time inference.
* **UI/UX:** Developed using **CustomTkinter**, providing a high-performance, GPU-accelerated graphical interface.



## ✨ Core Features
* **Live Biometric Scanning:** Real-time identification with an adaptive green bounding box for verified users.
* **Voice Interaction:** AI-synthesized voice feedback to greet users and confirm status.
* **Encrypted Database:** Stores facial biometric templates in a secure local directory (`stored_faces`).
* **Automated Logging:** Instant CSV-based data logging for attendance and security audits.
* **Analytics Dashboard:** Visual summary of enrollment and user activity.

## 📂 Project Structure
* `NileCortex_V-SECURE.exe` (or `.bat`): The main executable application.
* `stored_faces/`: Directory containing the database of registered biometric profiles.
* `models/`: Pre-trained neural network weights.
* `attendance_log.csv`: The automated database for activity history.
* `assets/`: Icons and corporate branding (NileCortex).



## 🛠️ Instructions for Evaluation
1. **Run the application:** Double-click the execution file.
2. **Registration:** Navigate to **REGISTER FACE**, enter a name, and capture the biometric profile.
3. **Verification:** Go to **LIVE SCANNER**; the system will identify the face and provide voice confirmation.
4. **Data Review:** Click **ANALYTICS** to view the generated logs.

---
> **Developer's Note:** This build is optimized for performance. To ensure maximum accuracy, please ensure the face is well-lit and directly facing the camera during the initial registration process.