# Job-Match-using-Langchain-and-ChromaDB

This is a Streamlit and LangChain-powered application that evaluates how well a user's profile matches with job descriptions. It analyzes resumes, GitHub portfolios, and job descriptions to provide match percentages, actionable insights, and tips for improvement.

## Features

- **Job Description Parsing**: Extracts key details such as role, experience, skills, and job descriptions from online job postings.
- **GitHub Portfolio Analysis**: Scans GitHub repositories for tech skills based on README.md and requirements.txt files.
- **Resume Parsing**: Extracts and analyzes information such as roles, experience, skills, education, and projects from uploaded resumes.
- **Profile Matching**: Provides a match percentage between your profile and the job description along with your portfolio.
- **Actionable Tips**: Offers resume improvement suggestions and guidance on writing tailored cover letters.

## Requirements

The project relies on the following Python libraries:

- `streamlit`
- `langchain`
- `langchain-google-genai`
- `chromadb`
- `pandas`
- `requests`
- `PyPDFLoader`
- `langchain_groq`

To install all requirements, run:
      ```bash
pip install -r requirements.txt

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Job-Match-using-Langchain-and-ChromaDB.git
    cd Job-Match-using-Langchain-and-ChromaDB
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set your API key as an environment variable:
  - For LLama 3.1 from Meta

    ```bash
    export groq_llama_api_key="your_groq_llama_api_key" 
    ```
    or 

  - For Gemini from Google

    ```bash
    export GOOGLE_API_KEY="your-google-api-key"
    ```


4. Set up your GitHub Token:
    - Go to GitHub and log in.
    - Navigate to your account settings by clicking on your profile picture in the top right corner.
    - In the left sidebar, click on "Developer settings".
    - Under "Personal access tokens", click "Generate new token".
    - Name the token (e.g., github_access_token), select the required   scopes (at least repo), and click "Generate token".
    - Copy the generated token and set it as an environment variable

    ```python
    export github_access_token="your_github_access_token"

    ```

5. Run the Streamlit app:
    ```bash
    streamlit run main.py
    ```
The app will open in your browser, ready for use.


# How It Works
1. **Enter Job Details**
   - Provide the URL of the job description.
   - Enter your GitHub username.
   - Specify the name of your vector database.
   - Upload your resume as a PDF.

2. **Data Processing**
   - The app extracts details from the job description using LangChain and parses your resume for relevant information.
   - It analyzes your GitHub repositories for tech skills and builds a vector database for quick lookup.

3. **Profile Matching**
   - Computes a match percentage between your profile and the job description.
   - Displays related GitHub projects that align with the job requirements.

4. **Actionable Insights**
   - Provides tips to improve your resume for the specific job.
   - Offers guidance on writing a tailored cover letter.

## Code Overview
### Job Description Analysis
- Extracts roles, skills, and experiences from job postings using LangChain prompts and Google Generative AI (Gemini).

### GitHub Portfolio Analysis
- Retrieves repositories via the GitHub API.
- Scans `README.md` and `requirements.txt` for technical skills.

### Resume Parsing
- Processes the resume using PyPDFLoader.
- Extracts details like skills, projects, and education.

### Profile Matching
- Builds a vector database using ChromaDB to store project details.
- Matches job description skills with GitHub projects and resume data.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contribution
Feel free to contribute by submitting pull requests or reporting issues. For questions or suggestions, contact the repository maintainer.
