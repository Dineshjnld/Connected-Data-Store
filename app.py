import streamlit as st
import hashlib

# Define classes
class DataStoreObject:
    def __init__(self, data, prev_object=None):
        self.index = prev_object.index + 1 if prev_object else 0
        self.data = data
        self.prev_hash = prev_object.current_hash if prev_object else '0000'
        self.correction_value = None
        self.current_hash = self.generate_hash()

    def generate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.index).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.prev_hash).encode('utf-8') +
            str(self.correction_value).encode('utf-8')  # Include correction value in hash calculation
        )
        return sha.hexdigest()

    def calculate_correction_value(self):
        # Dummy implementation for demonstration, replace with actual logic
        return "0000"

    def update_hash_with_correction(self):
        self.correction_value = self.calculate_correction_value()
        self.current_hash = self.generate_hash()

class ConnectedDataStore:
    def __init__(self):
        self.data_store = []

    def add_object(self, data):
        prev_object = self.data_store[-1] if self.data_store else None
        new_object = DataStoreObject(data, prev_object)
        new_object.update_hash_with_correction()  # Update hash with correction value
        self.data_store.append(new_object)
        return new_object

# Create instance of ConnectedDataStore or retrieve existing instance
if 'connected_data_store' not in st.session_state:
    st.session_state.connected_data_store = ConnectedDataStore()

# Streamlit UI
st.title('Connected Data Store')

data = st.text_input('Enter Data:', max_chars=1024)

if st.button('Add Data Store Object'):
    try:
        new_object = st.session_state.connected_data_store.add_object(data)
        st.success('Data Store Object added successfully!')
        st.write('Current Hash:', new_object.current_hash)
    except Exception as e:
        st.error(f'Error: {str(e)}')

# Display all blocks
st.title('All Blocks')
for block in st.session_state.connected_data_store.data_store:
    st.write(f'Index: {block.index}')
    st.write(f'Data: {block.data}')
    st.write(f'Previous Hash: {block.prev_hash}')
    st.write(f'Current Hash: {block.current_hash}')
    st.write('---')

# Add footer with information about the app
st.sidebar.title('About')
st.sidebar.info(
    '''
    This app demonstrates a simple implementation of a Connected Data Store.
    It allows users to add data store objects and performs hash calculations.
    '''
)
