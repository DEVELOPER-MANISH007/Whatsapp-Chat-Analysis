import streamlit as st
st.set_page_config(layout="wide") 
import preprocessor
import helper
import matplotlib.pyplot as plt
import plotly.express as px

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # file read
    bytes_data = uploaded_file.getvalue()
    
    # decode (safe way)
    data = bytes_data.decode("utf-8", errors="ignore")

    # preprocess
    df = preprocessor.preprocess(data)

   #  # show dataframe
   #  st.dataframe(df)

    # fetch uunique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("show analysis wrt ",user_list)

    if st.sidebar.button("show Analysis"):
       #! fetch helper.py(ke ander vala funcation)

       # stats Area
       num_messages,words,media,links =  helper.fetch_stats(selected_user,df) 
       st.title("Top  Statistics")
       col1,col2,col3,col4= st.columns(4)

       with col1:
        st.header("Total Messages")
        st.title(num_messages)
        with col2:
           st.header("Total Words")
           st.title(len(words))
        with col3:
           st.header("Total Meda")
           st.title((media))
        with col4:
           st.header("Total Link")
           st.title(len(links))
        
        #! monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation = 90)    
        st.pyplot(fig)

        # Daily Timeline 
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'])
        plt.xticks(rotation = 90)    
        st.pyplot(fig)

        # acticity Map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
         st.header("Most busy day")
         busy_day = helper.week_activity_map(selected_user,df)
         fig,ax = plt.subplots(figsize  = (12,8) )
         ax.bar(busy_day.index,busy_day.values)
         st.pyplot(fig, use_container_width=True)
        with col2:
         st.header("Most busy Month")
         busy_month = helper.monthly_activity_map(selected_user,df)
         fig,ax = plt.subplots(figsize  = (12,8) )
         ax.bar(busy_month.index,busy_month.values)
         st.pyplot(fig, use_container_width=True)

       
        #! finding the busiest users in the group (only for group chat)
        if selected_user  == 'Overall':
           st.title("Most Busy Users")
           x,new_df =  helper.most_busy_people(df)
           col1,col2 = st.columns(2)
           
           with col1:
            fig, ax = plt.subplots()   # 👈 bada size

            ax.bar(x.index, x.values, color='skyblue')

            ax.set_xlabel("Users")
            ax.set_ylabel("Messages")
            ax.set_title("Most Busy Users")

            plt.xticks(rotation=45)
            st.pyplot(fig)  
            with col2:
               st.dataframe(new_df)

         
        #? world clouad 

        st.title("Word cloud")
        df_wc = helper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
       most_common_df = helper.most_common_word(selected_user,df)
       fig,ax = plt.subplots(figsize=(4,2.5))
       ax.bar(most_common_df['Word'], most_common_df['Frequency'])
       plt.xticks(rotation  = 90)
       st.title("Most Common Words")
       st.pyplot(fig, use_container_width=False)
       st.dataframe(most_common_df)

      # emoji analysis
       emoji_df = helper.emoji_helper(selected_user,df)
       st.title("Emoji Analysis")
       col1,col2 = st.columns(2)

       with col1:
         st.dataframe(emoji_df)
       with  col2:
          if emoji_df.empty:
             st.info("No emojis found for selected chat/user.")
          else:
             pie_df = emoji_df.rename(columns={0: "emoji", 1: "count"})
             fig = px.pie(
                pie_df,
                values="count",
                names="emoji",
                title="Emoji Distribution"
             )
             fig.update_traces(textposition="inside", textinfo="percent+label")
             fig.update_layout(height=540)  # ~20% bigger than default
             st.plotly_chart(fig, use_container_width=True)



