import gradio as gr
import os
import io
from PIL import Image
import numpy as np
from huggingface_hub import InferenceClient
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

# Set up API keys
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Set up LLM
llm = ChatGroq(temperature=0, model_name='llama-3.1-8b-instant', groq_api_key=GROQ_API_KEY)
MAX_SEED = np.iinfo(np.int32).max
MAX_IMAGE_SIZE = 1024

# Initialize the Inference Client
client = InferenceClient("black-forest-labs/FLUX.1-schnell")

# Few-shot examples with input and detailed prompt
few_shot_examples = [
    ("A mood board for a luxury skincare brand with soft cream and gold tones, natural ingredients, and elegant packaging", 
     "Create a mood board for a high-end skincare brand, focusing on soft cream and gold tones. Include images of natural ingredients like lavender, honey, and shea butter. The packaging should be elegant, featuring minimalist designs and high-quality materials."),
    ("Create a birthday card for a friend", 
     "Design a vibrant birthday card for a close friend. Use bright colors like yellow and orange, with playful fonts and celebratory graphics like balloons and confetti. Include a heartfelt, personalized message."),
    ("An educational infographic showing the stages of the water cycle with bright, engaging visuals.", 
     "Develop an educational infographic that visually explains the stages of the water cycle: evaporation, condensation, precipitation, and collection. Use bright, engaging colors with clear labels and simple diagrams to make it easily understandable for students."),
    ("A minimalist workspace with a wooden desk, ergonomic chair, and a serene garden view.", 
     "Create a serene and minimalist workspace setup featuring a sleek wooden desk and an ergonomic chair. Position the workspace near a large window that offers a calming garden view with lush greenery and soft natural light.")
]

def generate_detailed_prompt(user_input):
    system_message = SystemMessage(content="""
    You are an AI assistant specialized in generating detailed image prompts. 
    Given a simple description, create an elaborate and detailed prompt that can be used to generate high-quality images.
    Your response should be concise and no longer than 3 sentences.
    Use the following examples as a guide for the level of detail and creativity expected:
    """ + "\n\n".join([f"Input: {input}\nOutput: {detailed}" for input, detailed in few_shot_examples]))
    
    human_message = HumanMessage(content=f"Generate a detailed image prompt based on this input, using no more than 3 sentences: {user_input}")
    
    response = llm.invoke([system_message, human_message])
    return response.content

def generate_image(prompt, width=1024, height=1024):
    try:
        result = client.text_to_image(
            prompt,
            width=width,
            height=height
        )
        
        if isinstance(result, Image.Image):
            return result
        else:
            return Image.open(io.BytesIO(result))
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def process_prompt(user_prompt):
    detailed_prompt = generate_detailed_prompt(user_prompt)
    return user_prompt, detailed_prompt, gr.update(visible=True), gr.update(visible=True)

def select_prompt(original_prompt, detailed_prompt, choice):
    return original_prompt if choice == "Original" else detailed_prompt

def on_example_click(example):
    user_prompt, detailed_prompt = example
    return user_prompt, detailed_prompt, gr.update(visible=True), gr.update(visible=True), gr.update(choices=["Original", "Detailed"], value="Original")

css = """
    body, html, #root, .gr-blocks, .gradio-container {
        height: 100%;
        margin: 0;
        padding: 0;
        background-color: black !important;  /* Full black background */
        color: #ffffff !important;  /* White text color */
    }
    .gradio-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100% !important;  /* Ensure the container fills the full width */
        max-width: 100% !important;  /* Remove any max-width restrictions */
    }
    #col-container {
        height: 100%;
        width: 100%;  /* Fill the entire width */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    #title {
        text-align: center;
        font-size: 34px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #ffffff !important;  /* White title color */
    }
    .gr-textbox, .gr-button, .gr-radio, .gr-markdown, .gr-example {
        background-color: #2c2c2e !important;  /* Dark gray background for inputs */
        color: #ffffff !important;  /* White text color */
        border-radius: 8px;
    }
    .gr-button {
        background-color: #bb86fc !important;  /* Purple button background */
        color: #ffffff !important;  /* White text on buttons */
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        cursor: pointer;
    }
    .gr-button:hover {
        background-color: #9b63ea !important;  /* Darker purple on hover */
    }
    .gr-examples-list .gr-example {
        color: #ffffff !important;  /* White text for examples */
    }
    footer {
        margin-top: 20px;
        text-align: center;
        color: #bb86fc;  /* Purple footer text color */
    }
    footer a {
        color: #bb86fc !important;  /* Purple links */
        text-decoration: none;
    }
    footer a:hover {
        text-decoration: underline;
    }
"""

with gr.Blocks(css=css, theme='gradio/soft') as demo:
    with gr.Column(elem_id="col-container"):
        gr.Markdown(
            "<h1 style='color:white;'>AI-Enhanced Image Generation</h1>", 
            elem_id="title"
        )

        
        with gr.Row():
            prompt = gr.Textbox(label="Initial Prompt", placeholder="Enter your prompt", elem_id="prompt", lines=2)
        
        generate_button = gr.Button("Generate Detailed Prompt", elem_id="generate_button")
        
        with gr.Row(visible=False, elem_id="prompt_selection_row") as prompt_selection_row:
            detailed_prompt = gr.Textbox(label="Detailed Prompt", elem_id="detailed_prompt", lines=3)
            prompt_choice = gr.Radio(["Original", "Detailed"], label="Choose Prompt", elem_id="prompt_choice")
        
        generate_image_button = gr.Button("Generate Image", elem_id="generate_image_button", visible=False)
        
        result = gr.Image(label="Generated Image", elem_id="result")
        
        examples = gr.Examples(
            examples=[(short, None) for short, _ in few_shot_examples],  # Only show short prompt
            inputs=[prompt],
            outputs=[prompt, detailed_prompt, prompt_selection_row, generate_image_button, prompt_choice],
            fn=on_example_click,
            cache_examples=False
        )

        footer_text = """
        <footer>
            <p>If you enjoyed the functionality of the app, please leave a like!</p>
            <p>To learn more about this app, visit our <a href="https://medium.com/@girishwangikar/crafting-visual-masterpieces-ais-creative-revolution-c6a7a21d86a4" target="_blank">blog</a>.</p>
            <p>Check out more on <a href="https://www.linkedin.com/in/girish-wangikar/" target="_blank">LinkedIn</a> |
            <a href="https://girishwangikar.github.io/Girish_Wangikar_Portfolio.github.io/" target="_blank">Portfolio</a></p>
        </footer>
        """

        gr.Markdown(footer_text)
        
    generate_button.click(
        process_prompt,
        inputs=[prompt],
        outputs=[prompt, detailed_prompt, prompt_selection_row, generate_image_button],
        api_name="generate_detailed_prompt"
    )
    
    generate_image_button.click(
        lambda p, d, c: generate_image(select_prompt(p, d, c)),
        inputs=[prompt, detailed_prompt, prompt_choice],
        outputs=[result],
        api_name="generate_image"
    )

demo.launch(share=True)
