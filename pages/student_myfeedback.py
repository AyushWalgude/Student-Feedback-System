import streamlit as st
import pandas as pd
from db import run_query

def show():
    st.subheader("📋 My Submitted Feedback")

    student_id = st.session_state.user["student_id"]

    my_fb = run_query("""
        SELECT t.name AS teacher, t.subject,
               f.teaching_quality, f.communication, f.punctuality,
               f.knowledge, f.overall_rating, f.comments, f.submitted_at
        FROM feedback f
        JOIN teachers t ON f.teacher_id = t.teacher_id
        WHERE f.student_id=%s
        ORDER BY f.submitted_at DESC
    """, (student_id,), fetch=True)

    if my_fb:
        df = pd.DataFrame(my_fb)
        df.columns = ["Teacher", "Subject", "Teaching", "Communication",
                      "Punctuality", "Knowledge", "Overall ⭐", "Comments", "Submitted At"]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.info(f"You have submitted **{len(my_fb)}** feedback record(s).")
    else:
        st.info("You haven't submitted any feedback yet. Go to 📝 Submit Feedback to get started.")
