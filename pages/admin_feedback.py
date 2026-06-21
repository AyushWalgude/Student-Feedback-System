import streamlit as st
import pandas as pd
from db import run_query

def show():
    st.subheader("📊 All Feedback Records")

    teachers = run_query("SELECT teacher_id, name FROM teachers ORDER BY name", fetch=True)
    filter_opts = {"All Teachers": None}
    filter_opts.update({t["name"]: t["teacher_id"] for t in teachers})

    col1, col2 = st.columns([2, 1])
    with col1:
        sel_filter = st.selectbox("Filter by Teacher", list(filter_opts.keys()))
    with col2:
        sort_by = st.selectbox("Sort By", ["Newest First", "Highest Rating", "Lowest Rating"])

    where  = "WHERE f.teacher_id=%s" if filter_opts[sel_filter] else ""
    params = (filter_opts[sel_filter],) if filter_opts[sel_filter] else ()
    order  = {
        "Newest First":   "f.submitted_at DESC",
        "Highest Rating": "f.overall_rating DESC",
        "Lowest Rating":  "f.overall_rating ASC"
    }[sort_by]

    rows = run_query(f"""
        SELECT t.name AS teacher, t.subject,
               f.teaching_quality, f.communication, f.punctuality,
               f.knowledge, f.overall_rating, f.comments, f.submitted_at
        FROM feedback f
        JOIN teachers t ON f.teacher_id = t.teacher_id
        {where}
        ORDER BY {order}
    """, params, fetch=True)

    if rows:
        df = pd.DataFrame(rows)
        df.columns = ["Teacher", "Subject", "Teaching", "Communication",
                      "Punctuality", "Knowledge", "Overall ⭐", "Comments", "Submitted At"]
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Delete feedback
        st.markdown("---")
        st.subheader("🗑️ Delete a Feedback Record")
        fb_list = run_query(f"""
            SELECT f.student_id, f.teacher_id, t.name AS teacher,
                   f.overall_rating, f.submitted_at
            FROM feedback f
            JOIN teachers t ON f.teacher_id = t.teacher_id
            {where}
            ORDER BY f.submitted_at DESC
        """, params, fetch=True)

        if fb_list:
            del_opts = {
                f"{r['teacher']} ⭐{r['overall_rating']} ({str(r['submitted_at'])})": (r["student_id"], r["teacher_id"])
                for r in fb_list
                }

            sel_del = st.selectbox("Select Feedback to Delete", list(del_opts.keys()))

            if st.button("🗑️ Delete This Feedback"):
                sid, tid = del_opts[sel_del]
                run_query(
                "DELETE FROM feedback WHERE student_id=%s AND teacher_id=%s",
                (sid, tid)
                )
                st.success("✅ Feedback deleted!")
                st.rerun()

        # Bar chart breakdown for single teacher
        if filter_opts[sel_filter]:
            st.markdown("---")
            st.subheader("📉 Category Breakdown")
            avg_row = run_query("""
                SELECT ROUND(AVG(teaching_quality),2) AS teaching,
                       ROUND(AVG(communication),2)    AS communication,
                       ROUND(AVG(punctuality),2)      AS punctuality,
                       ROUND(AVG(knowledge),2)        AS knowledge,
                       ROUND(AVG(overall_rating),2)   AS overall
                FROM feedback WHERE teacher_id=%s
            """, (filter_opts[sel_filter],), fetch=True)[0]

            avg_df = pd.DataFrame({
                "Category": ["Teaching", "Communication", "Punctuality", "Knowledge", "Overall"],
                "Score":    [avg_row["teaching"], avg_row["communication"],
                             avg_row["punctuality"], avg_row["knowledge"], avg_row["overall"]]
            })
            st.bar_chart(avg_df.set_index("Category"))
    else:
        st.info("No feedback records found.")
