import streamlit as st


import auth
from pages import (
    admin_dashboard,
    admin_teachers,
    admin_students,
    admin_feedback,
    admin_admins,
    student_feedback,
    student_myfeedback,
)


st.set_page_config(
    page_title="Student Feedback System",
    page_icon="🎓",
    layout="wide"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

    .title-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        color: white; padding: 2rem 2.5rem; border-radius: 16px;
        margin-bottom: 2rem; text-align: center;
    }
    .title-box h1 { font-size: 2rem; margin: 0; }
    .title-box p  { opacity: 0.8; margin: 0.4rem 0 0; }
    .role-badge-admin {
        background: #fff3cd; color: #856404; padding: 4px 14px;
        border-radius: 20px; font-size: 0.8rem; font-weight: 600;
        display: inline-block; margin-bottom: 1rem;
    }
    .role-badge-student {
        background: #d1ecf1; color: #0c5460; padding: 4px 14px;
        border-radius: 20px; font-size: 0.8rem; font-weight: 600;
        display: inline-block; margin-bottom: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 2rem; font-weight: 600;
        font-family: 'Poppins', sans-serif; width: 100%;
    }
    .stButton > button:hover { opacity: 0.9; }
            
    /*chnaged*/       
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

#  Session State Init 
for key, val in {
    "role": None,
    "user": None,
    "feedback_step": 1,
    "selected_student_id": None,
    "selected_student_name": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

#  Logout Helper 
def logout():
    for key in ["role", "user", "selected_student_id", "selected_student_name"]:
        st.session_state[key] = None
    st.session_state.feedback_step = 1
    st.rerun()

# Header 
st.markdown("""
<div class="title-box">
    <h1>🎓 Student Feedback System</h1>
    <p>Submit and manage faculty feedback</p>
</div>
""", unsafe_allow_html=True)

#not login
if not st.session_state.role:
    auth.show_auth_page()
    st.stop()

#login
with st.sidebar:
    if st.session_state.role == "admin":
        st.markdown(f"### 👋 {st.session_state.user['name']}")
        st.markdown(
            '<span style="background:#fff3cd;color:#856404;padding:3px 10px;'
            'border-radius:20px;font-size:0.8rem;font-weight:600;">🔐 Admin</span>',
            unsafe_allow_html=True
        )
        st.markdown("---")
        page = st.radio("Navigation", [
            "🏠 Dashboard",
            "📊 View Feedback",
            "👨‍🏫 Manage Teachers",
            "🧑‍🎓 Manage Students",
            "🔐 Manage Admins",
        ])

    else:  # student
        st.markdown(f"### 👋 {st.session_state.user['name']}")
        st.markdown(
            '<span style="background:#d1ecf1;color:#0c5460;padding:3px 10px;'
            'border-radius:20px;font-size:0.8rem;font-weight:600;">🎓 Student</span>',
            unsafe_allow_html=True
        )
        st.markdown("---")
        page = st.radio("Navigation", [
            "📝 Submit Feedback",
            "📋 My Feedback",
        ])

    st.markdown("---")
    if st.button("🚪 Logout"):
        logout()


#  Admin routes 
if st.session_state.role == "admin":
    if page == "🏠 Dashboard":
        admin_dashboard.show()
    elif page == "📊 View Feedback":
        admin_feedback.show()
    elif page == "👨‍🏫 Manage Teachers":
        admin_teachers.show()
    elif page == "🧑‍🎓 Manage Students":
        admin_students.show()
    elif page == "🔐 Manage Admins":
        admin_admins.show()

#  Student routes
elif st.session_state.role == "student":
    if page == "📝 Submit Feedback":
        student_feedback.show()
    elif page == "📋 My Feedback":
        student_myfeedback.show()

#  Footer 
st.markdown("---")
st.markdown(
    "<center><small>🎓 Student Feedback System | AYUSH | SAI | PRUTHVI |HARSHAD | VEDANT |</small></center>",
    unsafe_allow_html=True
)
