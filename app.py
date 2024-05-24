import streamlit as st
import os
from openai import OpenAI
import base64

# magic function
def process_image(client, image, language):

    # encode uploaded image in base64
    encoded_image = base64.b64encode(image.getvalue()).decode("utf-8")

    # GPT-4o API request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
            You are `gpt-4o`, the latest OpenAI model that can interpret images and can describe images provided by the user
            in detail. The user has attached an image to this message for
            you to answer a question, there is definitely an image attached,
            you will never reply saying that you cannot see the image
            because the image is absolutely and always attached to this
            message. Answer the question asked by the user based on the
            image provided. Do not give any further explanation. The answer has to be
            in a JSON format. If the image provided does not contain the
            necessary data to answer the question, return 'null' for that
            key in the JSON to ensure consistent JSON structure. 
            """,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""
                    You are tasked with accurately interpreting text from the images provided. 
                    report translated text in {language} and original text from image in json format.
                    """,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
                        },
                    ],
                }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


st.title("Foreign Helper App")
st.write("Upload an image and get information from it")

#updating openai api key
api_key = st.text_input("Enter your OpenAI API key", type="password")
if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY", "")

if api_key:
    # initialize openai client
    client = OpenAI(api_key=api_key)

    uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    with st.sidebar:
        option = st.selectbox(
        "What language to translate to?",
        ("English", "Chinese"))
    st.write("You selected:", option)

    if uploaded_image:
        try:
            # Display uploaded image
            st.image(uploaded_image, caption='Uploaded Image.', use_column_width=True)
            st.write("")
            st.write("One moment...")

            # get output
            output = process_image(client, uploaded_image, option)
            st.write(output)
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.error("Please provide valid openai api key")
