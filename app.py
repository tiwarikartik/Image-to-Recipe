import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import base64
import json

from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv(find_dotenv())
google_api_key = os.getenv("GOOGLE_API_KEY")

llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)


def image_to_text(uploaded_file):
    """
    Identifies ingredients from an image using Google's multimodal AI
    by Base64 encoding the image data.
    """

    llm_vision = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    file_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type
    base64_image = base64.b64encode(file_bytes).decode("utf-8")
    image_url = f"data:{mime_type};base64,{base64_image}"
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "You are an expert at identifying food items from an image.\n"
                    "Analyze the provided image and list all the edible ingredients you can identify.\n"
                    "Please list the ingredients as a comma-separated string. Do not add any other text, just the ingredients."
                ),
            },
            {"type": "image_url", "image_url": {"url": image_url}},
        ]
    )
    response = llm_vision.invoke([message])
    ingredients_text = response.content
    print(f"Identified Ingredients (Google AI):: {ingredients_text}")
    return ingredients_text


def generate_recipe(ingredients):
    """
    Generates a recipe as a JSON object based on a list of ingredients.
    """
    template = """
    You are an extremely knowledgeable nutritionist and chef. Your task is to generate a recipe based on a list of ingredients.
    The user will provide the ingredients: {ingredients}
    
    If the ingredients list is short (less than 3), you may add a few complementary healthy items. but if it is more than 3 stick to the ingredients detected.

    Your response MUST be a single, well-formed JSON object. Do not include any text, explanation, or markdown formatting outside of the JSON object.
    
    The JSON object must have the following structure:
    {{
      "title": "Name of the Meal",
      "ideal_for": "not more than two words, e.g., 'Quick Lunch', 'Post-Workout', 'Healthy Dinner'",
      "preparation_time": "Estimated time (e.g., '15-20 min', '1-1:15 hr')",
      "difficulty": "Easy, Medium, or Hard",
      "ingredients": ["Ingredient 1", "Ingredient 2", "Ingredient 3"],
      "kitchen_tools": ["Tool 1", "Tool 2", "Tool 3"],
      "instructions": ["Step 1 detailed description.", "Step 2 detailed description.", "Step 3 detailed description...."],
      "macros": " Generate the estimated macros of the ingredients in the markdown tabular format"
    }}
    Make sure the json is formatted properly and properly validated.Ensure proper bracket placement when dealing with lists
    """
    prompt = PromptTemplate(template=template, input_variables=["ingredients"])
    recipe_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    try:
        response_text = recipe_chain.invoke({"ingredients": ingredients})
        json_string = (
            response_text["text"].strip().replace("```json", "").replace("```", "")
        )
        recipe_json = json.loads(json_string)
        return recipe_json
    except json.JSONDecodeError as e:
        st.error(
            f"Failed to decode the recipe from the AI. Please try again. Error: {e}"
        )
        print(f"JSON Decode Error. Raw response was:\n{response_text['text']}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None


def main():
    """
    Main function to run the Streamlit application.
    """
    st.set_page_config(page_title="Image to Recipe Generator", page_icon="🍲")

    st.sidebar.header("Upload Your Ingredients")
    uploaded_file = st.sidebar.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png", "webp"]
    )

    st.title("Image to Recipe Generator 🍲")
    st.header("Get a Recipe from a Picture!")

    if uploaded_file is not None:
        display_bytes = uploaded_file.getvalue()
        st.sidebar.image(
            display_bytes, caption="Your Uploaded Image", use_container_width=True
        )
        with st.spinner("Detecting Ingredients in the Image...."):
            ingredients = image_to_text(uploaded_file)
        st.subheader("Detected Ingredients")
        st.info(ingredients)
        with st.spinner("Creating a recipe for you...."):
            recipe_data = generate_recipe(ingredients)
        if recipe_data:
            st.subheader(recipe_data.get("title", "Your Recipe"))

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.metric(
                    label="**Best For**", value=recipe_data.get("ideal_for", "N/A")
                )
            with col2:
                st.metric(
                    label="**Time**", value=recipe_data.get("preparation_time", "N/A")
                )
            with col3:
                st.metric(
                    label="**Difficulty**", value=recipe_data.get("difficulty", "N/A")
                )

            with st.expander("**Ingredients**", expanded=True):
                ingredients_list = "\n".join(
                    [f"- {item}" for item in recipe_data.get("ingredients", [])]
                )
                st.markdown(ingredients_list)

            with st.expander("**Kitchen Tools Needed**", expanded=True):
                tools_list = "\n".join(
                    [f"- {tool}" for tool in recipe_data.get("kitchen_tools", [])]
                )
                st.markdown(tools_list)

            with st.expander("**Cooking Instructions**", expanded=True):
                instructions_list = "\n".join(
                    [
                        f"{i}. {instruction}"
                        for i, instruction in enumerate(
                            recipe_data.get("instructions", []), 1
                        )
                    ]
                )
                st.markdown(instructions_list)

            with st.expander("**Macros**", expanded=True):
                st.markdown(
                    recipe_data.get("macros", "Not available."), width="stretch"
                )
    else:
        st.info("Please upload an image of your ingredients to get started.")


if __name__ == "__main__":
    main()
