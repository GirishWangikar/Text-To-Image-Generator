# AI-Enhanced Image Generation

To know more, check out my blog - [Crafting Visual Masterpieces: AI’s Creative Revolution](https://medium.com/@girishwangikar/crafting-visual-masterpieces-ais-creative-revolution-c6a7a21d86a4)

This project demonstrates an AI-enhanced image generation application using Gradio, Hugging Face, and LangChain. It allows users to input a simple prompt, which is then expanded into a detailed description using a language model, and finally used to generate an image.

## Features

- **User-friendly Interface**: Built with Gradio for an interactive and intuitive user experience.
- **AI-Powered Prompt Enhancement**: Utilizes LangChain and Groq to transform basic prompts into detailed descriptions.
- **Image Generation**: Leverages Hugging Face's Inference API for high-quality image creation.
- **Example Prompts**: Pre-loaded prompts are available for quick testing and inspiration.
- **Customizable Image Dimensions**: Users can adjust the image size to meet their specific needs.
- **Dark Mode UI**: A visually appealing dark mode interface for comfortable usage.

## Prerequisites

Before running this application, ensure you have the following:

- Python 3.7+
- Gradio
- Pillow
- NumPy
- Hugging Face Hub
- LangChain
- API key

## Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/GirishWangikar/Text-To-Image-Generator
    cd ai-enhanced-image-generation
    ```

2. **Install the required packages:**

    ```bash
    pip install gradio pillow numpy huggingface_hub langchain-groq
    ```

3. **Set up your API key as an environment variable:**

    ```bash
    export API_KEY='your_api_key_here'
    ```

## Usage

1. **Run the application:**

    ```bash
    python app.py
    ```

2. **Open your web browser and navigate to the URL provided in the console output.**

3. **Generate a detailed prompt:**

   - Enter a prompt in the text box and click "Generate Detailed Prompt" to see an AI-enhanced version of your prompt.

4. **Generate an image:**

   - Choose between the original or detailed prompt, then click "Generate Image" to create an image based on the selected prompt.

5. **Explore Examples:**

   - Use the provided examples for inspiration and see the potential of AI-enhanced image generation.


## Contact

Created by [Girish Wangikar](https://www.linkedin.com/in/girish-wangikar/)

Check out more on [LinkedIn](https://www.linkedin.com/in/girish-wangikar/) | [Portfolio](https://girishwangikar.github.io/Girish_Wangikar_Portfolio.github.io/) | [Technical Blog - Medium](https://medium.com/@girishwangikar/crafting-visual-masterpieces-ais-creative-revolution-c6a7a21d86a4)


