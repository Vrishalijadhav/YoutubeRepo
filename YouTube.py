#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install google-api-python-client
import streamlit as st
import googleapiclient.discovery
import pymongo

# Set up the YouTube API client
youtube = googleapiclient.discovery.build('youtube', 'v3', cache_discovery=False)

# Set up the MongoDB client
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['Youtube_Data_Lake']
collection = db['YouTube']

# Streamlit app
def main():
    st.title('YouTube Channel Migration')
    channel_id = st.text_input('Enter YouTube Channel ID')

    if st.button('Get Channel Details'):
        channel_data = get_channel_details(channel_id)
        if channel_data:
            st.subheader('Channel Details')
            st.write(channel_data)
            if st.button('Migrate Channel'):
                migrate_channel(channel_data)
                st.success('Channel migrated successfully!')

def get_channel_details(channel_id):
    try:
        response = youtube.channels().list(part='snippet,statistics', id=channel_id).execute()
        if 'items' in response and len(response['items']) > 0:
            channel_data = response['items'][0]
            return channel_data
    except googleapiclient.errors.HttpError as e:
        st.error('Error occurred while retrieving channel details: ' + str(e))

def migrate_channel(channel_data):
    try:
        collection.insert_one(channel_data)
    except pymongo.errors.PyMongoError as e:
        st.error('Error occurred while migrating channel: ' + str(e))

if __name__ == '__main__':
    main()


# In[ ]:




