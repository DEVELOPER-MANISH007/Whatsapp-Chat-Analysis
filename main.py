import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

import helper
import preprocessor

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.title("WhatsApp Chat Analyzer")

st.sidebar.title("Upload and Settings")
uploaded_file = st.sidebar.file_uploader("Choose a chat export (.txt)")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8", errors="ignore")
    df = preprocessor.preprocess(data)

    user_list = df["user"].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis", type="primary"):
        filtered_df = df.copy()

        num_messages, words, media, links = helper.fetch_stats(selected_user, filtered_df)
        avg_words_per_message, longest_message_words = helper.additional_stats(selected_user, filtered_df)

        st.subheader("Top Statistics")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Total Messages", f"{num_messages:,}")
        col2.metric("Total Words", f"{len(words):,}")
        col3.metric("Media Shared", f"{media:,}")
        col4.metric("Links Shared", f"{len(links):,}")
        col5.metric("Avg Words/Msg", avg_words_per_message)
        col6.metric("Longest Msg (words)", longest_message_words)

        st.markdown("---")
        st.subheader("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, filtered_df)
        fig, ax = plt.subplots(figsize=(14, 4.5))
        ax.plot(timeline["time"], timeline["message"], color="#1f77b4", linewidth=2)
        ax.set_xlabel("Month")
        ax.set_ylabel("Messages")
        ax.tick_params(axis="x", rotation=60)
        ax.grid(alpha=0.3, linestyle="--")
        st.pyplot(fig, use_container_width=True)

        st.subheader("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, filtered_df)
        fig, ax = plt.subplots(figsize=(14, 4.5))
        ax.plot(
            daily_timeline["only_date"],
            daily_timeline["message"],
            color="#2ca02c",
            linewidth=1.8,
        )
        ax.set_xlabel("Date")
        ax.set_ylabel("Messages")
        ax.tick_params(axis="x", rotation=60)
        ax.grid(alpha=0.3, linestyle="--")
        st.pyplot(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, filtered_df)
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.bar(busy_day.index, busy_day.values, color="#636EFA")
            ax.set_ylabel("Messages")
            ax.tick_params(axis="x", rotation=45)
            st.pyplot(fig, use_container_width=True)

        with col2:
            st.markdown("#### Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user, filtered_df)
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.bar(busy_month.index, busy_month.values, color="#EF553B")
            ax.set_ylabel("Messages")
            ax.tick_params(axis="x", rotation=45)
            st.pyplot(fig, use_container_width=True)

        st.subheader("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, filtered_df)
        fig, ax = plt.subplots(figsize=(14, 4.5))
        sns.heatmap(user_heatmap, cmap="YlGnBu", linewidths=0.2, ax=ax)
        ax.set_xlabel("Time Period")
        ax.set_ylabel("Day")
        st.pyplot(fig, use_container_width=True)

        st.subheader("Hourly Activity")
        hourly_df = helper.hourly_activity(selected_user, filtered_df)
        fig, ax = plt.subplots(figsize=(14, 4.5))
        ax.plot(hourly_df.index, hourly_df.values, marker="o", color="#AB63FA")
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Messages")
        ax.set_xticks(range(0, 24))
        ax.grid(alpha=0.3, linestyle="--")
        st.pyplot(fig, use_container_width=True)

        if selected_user == "Overall":
            st.markdown("---")
            st.subheader("Most Busy Users")
            x, new_df = helper.most_busy_people(filtered_df)
            col1, col2 = st.columns([2, 1])

            with col1:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(x.index, x.values, color="skyblue")
                ax.set_xlabel("Users")
                ax.set_ylabel("Messages")
                ax.tick_params(axis="x", rotation=45)
                st.pyplot(fig, use_container_width=True)

            with col2:
                st.dataframe(new_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user, filtered_df)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig, use_container_width=True)

        st.subheader("Most Common Words")
        most_common_df = helper.most_common_word(selected_user, filtered_df)
        fig, ax = plt.subplots(figsize=(14, 4.5))
        ax.bar(most_common_df["Word"], most_common_df["Frequency"], color="#00CC96")
        ax.set_xlabel("Words")
        ax.set_ylabel("Frequency")
        ax.tick_params(axis="x", rotation=70)
        st.pyplot(fig, use_container_width=True)
        st.dataframe(most_common_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, filtered_df)
        col1, col2 = st.columns([1, 2])

        with col1:
            st.dataframe(emoji_df, use_container_width=True, hide_index=True)

        with col2:
            if emoji_df.empty:
                st.info("No emojis found for selected chat/user.")
            else:
                pie_df = emoji_df.rename(columns={0: "emoji", 1: "count"})
                fig = px.pie(
                    pie_df,
                    values="count",
                    names="emoji",
                    title="Emoji Distribution",
                )
                fig.update_traces(textposition="inside", textinfo="percent+label")
                fig.update_layout(height=520)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Shared Links")
        links_df = helper.links_dataframe(selected_user, filtered_df)
        if links_df.empty:
            st.info("No links found in selected range.")
        else:
            st.dataframe(links_df, use_container_width=True, hide_index=True)

        st.download_button(
            label="Download Filtered Chat as CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name=f"chat_analysis_{selected_user}.csv",
            mime="text/csv",
        )
