import streamlit as st
from db import run_query

def show():
    st.subheader("📝 Submit Your Feedback")

    student_id = st.session_state.user["student_id"]
 
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.feedback_step == 1:
            st.markdown("### 🔵 Step 1: Confirm Identity")
        else:
            st.markdown("### ✅ Step 1: Confirmed")
    with col2:
        if st.session_state.feedback_step == 2:
            st.markdown("### 🔵 Step 2: Rate Teacher")
        else:
            st.markdown("### ⬜ Step 2: Rate Teacher")

    st.markdown("---")

    # STEP 1 — Confirm identity
    
    if st.session_state.feedback_step == 1:
        user = st.session_state.user
        st.info(
            f"**Name:** {user['name']}  \n"
            f"**Student ID:** {user['student_id']}  \n"
            f"**Department:** {user['department']}"
        )
        if st.button("✅ Confirm & Continue →"):
            st.session_state.selected_student_id   = user["student_id"]
            st.session_state.selected_student_name = user["name"]
            st.session_state.feedback_step = 2
            st.rerun()

    # STEP 2 — Select teacher & rate
    
    elif st.session_state.feedback_step == 2:
        st.success(
            f"🧑‍🎓 **{st.session_state.selected_student_name}** "
            f"({st.session_state.selected_student_id})"
        )

        teachers = run_query(
            "SELECT teacher_id, name, subject, department FROM teachers ORDER BY name",
            fetch=True
        )
        if not teachers:
            st.warning("No teachers available. Contact admin.")
            st.stop()

        already_rated = run_query(
            "SELECT teacher_id FROM feedback WHERE student_id=%s",
            (student_id,), fetch=True
        )
        rated_ids = {r["teacher_id"] for r in already_rated}
        available = [t for t in teachers if t["teacher_id"] not in rated_ids]
        rated     = [t for t in teachers if t["teacher_id"] in rated_ids]

        if rated:
            with st.expander(f"✅ Already rated ({len(rated)} teachers)"):
                for t in rated:
                    st.markdown(f"- ~~{t['name']} — {t['subject']}~~")

        if not available:
            st.success("🎉 You have rated all teachers!")
            if st.button("← Back"):
                st.session_state.feedback_step = 1
                st.rerun()
            st.stop()

        teacher_opts = {
            f"{t['name']} — {t['subject']} ({t['department']})": t["teacher_id"]
            for t in available
        }

        with st.form("feedback_form", clear_on_submit=True):
            sel_teacher = st.selectbox("👨‍🏫 Select Teacher", list(teacher_opts.keys()))

            st.markdown("---")
            st.markdown("#### ⭐ Rate the Teacher (1 = Poor, 5 = Excellent)")

            r1, r2 = st.columns(2)
            with r1:
                tq = st.slider("📚 Teaching Quality", 1, 5, 3)
                cm = st.slider("🗣️ Communication Skills", 1, 5, 3)
                pu = st.slider("⏰ Punctuality", 1, 5, 3)
            with r2:
                kn = st.slider("🧠 Subject Knowledge", 1, 5, 3)
                ov = st.slider("🌟 Overall Rating", 1, 5, 3)

            st.markdown("---")
            comments = st.text_area("💬 Comments (optional)", height=100,
                                    placeholder="Share your experience...")

            col_back, col_submit = st.columns([1, 3])
            with col_back:
                go_back = st.form_submit_button("← Back")
            with col_submit:
                submitted = st.form_submit_button("✅ Submit Feedback")

            if go_back:
                st.session_state.feedback_step = 1
                st.rerun()

            if submitted:
                tid = teacher_opts[sel_teacher]
                run_query("""
                    INSERT INTO feedback
                        (student_id, teacher_id, teaching_quality, communication,
                         punctuality, knowledge, overall_rating, comments)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (student_id, tid, tq, cm, pu, kn, ov, comments))
                st.success("🎉 Feedback submitted successfully!")
                st.balloons()
                st.rerun()
