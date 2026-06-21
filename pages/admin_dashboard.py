import streamlit as st
import pandas as pd
from db import run_query

def show():
    st.subheader("📈 Overview")

    total_feedback = run_query("SELECT COUNT(*) AS cnt FROM feedback", fetch=True)[0]["cnt"]
    total_students = run_query("SELECT COUNT(*) AS cnt FROM students", fetch=True)[0]["cnt"]
    total_teachers = run_query("SELECT COUNT(*) AS cnt FROM teachers", fetch=True)[0]["cnt"]
    avg_result     = run_query("SELECT AVG(overall_rating) AS avg FROM feedback", fetch=True)[0]["avg"]
    avg_rating     = round(float(avg_result), 2) if avg_result else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📝 Total Feedback", total_feedback)
    c2.metric("🧑‍🎓 Students", total_students)
    c3.metric("👨‍🏫 Teachers", total_teachers)
    c4.metric("⭐ Avg Rating", f"{avg_rating} / 5")

    st.markdown("---")

    # Top rated teachers
    st.subheader("🏆 Top Rated Teachers")
    top = run_query("""
        SELECT t.name, t.subject, t.department,
               ROUND(AVG(f.overall_rating), 2) AS avg_rating,
               COUNT(f.student_id) AS total
        FROM feedback f
        JOIN teachers t ON f.teacher_id = t.teacher_id
        GROUP BY t.teacher_id
        ORDER BY avg_rating DESC
        LIMIT 5
    """, fetch=True)

    if top:
        df = pd.DataFrame(top)
        df.columns = ["Teacher", "Subject", "Department", "Avg Rating ⭐", "Feedbacks"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No feedback submitted yet.")

    # Recent feedback
    st.subheader("🕐 Recent Feedback")
    recent = run_query("""
        SELECT t.name AS teacher, f.overall_rating,
               LEFT(f.comments, 60) AS comment, f.submitted_at
        FROM feedback f
        JOIN teachers t ON f.teacher_id = t.teacher_id
        ORDER BY f.submitted_at DESC
        LIMIT 8
    """, fetch=True)

    if recent:
        df2 = pd.DataFrame(recent)
        df2.columns = ["Teacher", "Rating ⭐", "Comment", "Submitted At"]
        st.dataframe(df2, use_container_width=True, hide_index=True)
    else:
        st.info("No recent feedback.")
