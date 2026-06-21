import streamlit as st
from db import run_query, verify_admin, verify_student

def show_auth_page():
    """Shows login/register page when user is not logged in."""

    login_mode = st.radio(
        "Select Portal",
        ["🎓 Student Portal", "🔐 Admin Portal"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown("---")

    #  STUDENT PORTAL 
    if login_mode == "🎓 Student Portal":
        tab_login, tab_register = st.tabs(["🔑 Student Login", "📝 Register Account"])

        with tab_login:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.markdown('<span class="role-badge-student">🎓 Student Login</span>', unsafe_allow_html=True)
            email    = st.text_input("Email", key="s_email")
            password = st.text_input("Password", type="password", key="s_pass")
            if st.button("Login", key="s_login_btn"):
                if email and password:
                    student = verify_student(email, password)
                    if student:
                        st.session_state.role = "student"
                        st.session_state.user = student
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password.")
                else:
                    st.error("Please fill in all fields.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_register:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.markdown('<span class="role-badge-student">📝 Create Account</span>', unsafe_allow_html=True)
            st.info("Your Student ID must already be added by the Admin.")
            reg_sid   = st.text_input("Student ID (e.g. CS101)", key="reg_sid")
            reg_email = st.text_input("Email", key="reg_email")
            reg_pass  = st.text_input("Create Password", type="password", key="reg_pass")
            reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2")
            if st.button("Register", key="reg_btn"):
                if reg_sid and reg_email and reg_pass and reg_pass2:
                    if reg_pass != reg_pass2:
                        st.error("❌ Passwords do not match.")
                    else:
                        student = run_query(
                            "SELECT * FROM students WHERE student_id=%s AND email=%s",
                            (reg_sid,reg_email), fetch=True
                        )
                        if not student:
                            st.error("❌ Student ID or email not found. Contact your Admin.")
                        elif student[0]["is_registered"]:
                            st.error("❌ This Student ID is already registered.")
                        else:
                            run_query(
                                "UPDATE students SET  password=%s, is_registered=TRUE WHERE student_id=%s",
                                ( reg_pass, reg_sid)#email=%s,
                            )
                            st.success("✅ Account created! You can now login.")
                else:
                    st.error("Please fill in all fields.")
            st.markdown('</div>', unsafe_allow_html=True)

    #  ADMIN PORTAL
    else:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<span class="role-badge-admin">🔐 Admin Login</span>', unsafe_allow_html=True)
        email    = st.text_input("Admin Email", key="a_email")
        password = st.text_input("Password", type="password", key="a_pass")
        if st.button("Login as Admin", key="a_login_btn"):
            if email and password:
                admin = verify_admin(email, password)
                if admin:
                    st.session_state.role = "admin"
                    st.session_state.user = admin
                    st.rerun()
                else:
                    st.error("❌ Invalid admin credentials.")
            else:
                st.error("Please fill in all fields.")
        st.markdown('</div>', unsafe_allow_html=True)
