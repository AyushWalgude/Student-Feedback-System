# Student-Feedback-System
A full-stack Student Feedback System built with Streamlit, Python, and MySQL. Features role-based authentication (Admin &amp; Student), student self-registration, 5-category feedback ratings, real-time analytics dashboard, and complete CRUD management — all without writing HTML/CSS.
# 🎓 Student Feedback System

A full-stack web application for collecting and managing student feedback on faculty, built entirely in Python using Streamlit and MySQL.

## ✨ Features
- 🔐 Role-based authentication (Admin & Student portals)
- 📝 Student self-registration with ID verification
- ⭐ 5-category feedback ratings (Teaching, Communication, Punctuality, Knowledge, Overall)
- 📊 Admin dashboard with stats, top-rated teachers, and analytics charts
- 🗑️ Full CRUD — add/view/delete students, teachers, feedback, and admins
- 🚫 Duplicate feedback prevention per student-teacher pair

## 🛠️ Tech Stack
- **Frontend:** Streamlit (pure Python, no HTML/CSS)
- **Backend:** Python
- **Database:** MySQL

## 🚀 Quick Start
bash
pip install -r requirements.txt<br>
mysql -u root -p < database.sql<br>
streamlit run app.py<br>


## 📁 Project Structure

student_feedback/<br>
├── app.py            # Main entry point<br>
├── db.py             # Database connection<br>
├── auth.py           # Login & registration<br>
└── pages/            # Modular page components<br>


## 📄 Documentation
Full project documentation available in `StudentFeedbackSystem_Documentation.docx`

## NOTE
login first with admin's id and password which is add in database.
