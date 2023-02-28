import streamlit as st
import os 
from streamlit_cropper import st_cropper
import itertools
from st_clickable_images import clickable_images
import base64
from PIL import Image
import random
import copy

st.set_page_config(layout="wide")

#DATA_PATH = '../data/oxbuild_images-v1/'
# DATA_PATH = '/cs336/data/'

st.title('Image retrieval')

def init_image_path():
    imgs_p = []
    # for file in os.listdir(DATA_PATH):
    #     if not file.endswith("jpg"):
    #         continue
    #     imgs_p.append(DATA_PATH + file)
    imgs_p.append("/cs336/query/query.jpg")
    return imgs_p

def show_cropper(path):

    img = Image.open(path)
    
    cropped_img = st_cropper(img, realtime_update=True, box_color='#0000FF', aspect_ratio=None)
    # Manipulate cropped image at will
    st.write("Preview")
    _ = cropped_img.thumbnail((150,150))
    st.image(cropped_img)
    return cropped_img

# INSERT RETRIEVAL MODEL HERE
def retrieve_image(query, data):
    new_data = copy.deepcopy(data)
    random.shuffle(new_data)
    return new_data

def demonstrate_image_pagination():

    imgs_p = init_image_path()
    image_iterator = itertools.islice(enumerate(imgs_p), 0, 10)
    indice_on_page, images_on_page = map(list, zip(*image_iterator))

    new_indice_on_page = []

    tab1, tab2 = st.tabs(['Select query', 'Results'])
    results = []
    with tab1:
        # col1, col2 = st.columns(2)
        # with col1:
            
        st.write("Upload image")
        uploaded_file = st.file_uploader("Choose file", type=['png','jpeg','jpg'])
        if uploaded_file is not None:
            with open(os.path.join("/cs336/query/query.jpg"),"wb") as f: 
                f.write(uploaded_file.getbuffer())

        img_encoded = []
        with open(os.path.join("/cs336/query/query.jpg"), "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            img_encoded.append(f"data:image/jpeg;base64,{encoded}")


        clicked = clickable_images(paths = img_encoded,     
            #titles=[f"Image #{str(i)}" for i,j in enumerate(images_on_page)],
            titles=new_indice_on_page,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "300px"},
        )
        
        st.markdown("Cropped query image")
        cropped = show_cropper(images_on_page[clicked])
            

    with tab2:
        st.image(cropped, caption='query')
        num = int(st.text_input('Input number of retrieved images to show: ', 50))
        if st.button(label='Search'): 
            results = retrieve_image(imgs_p[clicked], imgs_p)
        st.image(results[:num], width=200, caption=[str(i) for i in range(min(num, len(results)))])

if __name__ == '__main__':
    demonstrate_image_pagination()