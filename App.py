#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st


# In[6]:


from googleapiclient.discovery import build


# In[7]:


from pymongo import MongoClient


# In[8]:


def get_channel_details(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    response = youtube.channels().list(part='snippet,statistics', id=channel_id).execute()
    channel = response['items'][0]
    return channel


# In[11]:


def main():
    st.title("YouTube Channel Migration")

    # API key input
    api_key = st.text_input("Enter your YouTube API keyL:")

    # Channel ID input
    channel_id = st.text_input("Enter the YouTube channel ID:")

    if st.button("Retrieve Channel Details"):
        channel = get_channel_details(api_key, channel_id)
        st.write("Channel Details:")
        st.write(f"Title: {channel['snippet']['title']}")
        st.write(f"Description: {channel['snippet']['description']}")
        st.write(f"Subscribers: {channel['statistics']['subscriberCount']}")

        # Connect to MongoDB
        collection = connect_to_mongodb("mongodb://localhost:27017/", "youtube_data_lake", "channels")

        if st.button("Migrate Channel"):
            collection.insert_one(channel)
            st.write("Channel migrated successfully!")

if __name__ == "__main__":
    main()


# In[ ]:




