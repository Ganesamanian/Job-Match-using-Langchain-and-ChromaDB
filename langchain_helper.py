import os
import uuid
import chromadb
import requests
import pandas as pd
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.document_loaders import PyPDFLoader

llama_api_key = os.getenv("groq_llama_api_key")
google_api_key = os.getenv("google_api_key")

llm_llama = ChatGroq(model = "llama-3.1-70b-versatile",
                     temperature= 0,
                     max_tokens= None,
                     timeout=None,
                     groq_api_key = llama_api_key,
                     max_retries=2,
                        
)

llm_gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


# Function to extract tech skills from README or requirements.txt
def get_github_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {
    'Authorization': 'token <Enter_your_token>'
        }
    response = requests.get(url, headers=headers)
    
    # Check if the response is valid
    if response.status_code != 200:
        print(f"Error: Unable to fetch repositories for {username}. HTTP Status Code: {response.status_code}")
        return pd.DataFrame()

    repos = response.json()
    
    skills_keywords = {
        'AWS': ['aws', 'amazon web services'],
        'Streamlit': ['streamlit'],
        'NLP': ['nlp', 'natural language processing'],
        'Computer Vision': ['opencv', 'cv', 'computer vision'],
        'LLM': ['large language model', 'transformer'],
        'TensorFlow': ['tensorflow'],
        'PyTorch': ['pytorch'],
        'Scikit-learn': ['scikit-learn', 'sklearn'],
        'Keras': ['keras'],
        'Matplotlib': ['matplotlib'],
        'Pandas': ['pandas'],
        'NumPy': ['numpy'],
        'Docker': ['docker'],
        'Kubernetes': ['kubernetes'],
        'Flask': ['flask'],
        'SQL': ['sql'],
        'Git': ['git'],
        'Machine Learning': ['machine learning'],
        'Deep Learning': ['deep learning'],
        'Data Engineering': ['data engineering'],
        'Cloud Computing': ['cloud', 'azure', 'gcp'],
    }

    repo_data = []
    
    for repo in repos:
        if isinstance(repo, dict):  # Ensure that repo is a dictionary
            repo_url = repo.get('html_url', '')
            primary_language = repo.get('language', 'Not specified')  # Extract primary language
            if primary_language == "Jupyter Notebook":
                primary_language = "Python"  # Replace Jupyter Notebook with Python
            
            readme_url = f"https://raw.githubusercontent.com/{username}/{repo['name']}/main/README.md"
            req_url = f"https://raw.githubusercontent.com/{username}/{repo['name']}/main/requirements.txt"
            
            tech_stack = set()

            # Check README.md for tech skills
            readme_response = requests.get(readme_url, headers=headers)
            if readme_response.status_code == 200:
                readme_text = readme_response.text.lower()
                for skill, keywords in skills_keywords.items():
                    if any(keyword in readme_text for keyword in keywords):
                        tech_stack.add(skill)

            # Check requirements.txt for tech skills
            req_response = requests.get(req_url, headers=headers)
            if req_response.status_code == 200:
                req_text = req_response.text.lower()
                for skill, keywords in skills_keywords.items():
                    if any(keyword in req_text for keyword in keywords):
                        tech_stack.add(skill)

            tech_stack = ', '.join(tech_stack) if tech_stack else "Not specified"
            
            if tech_stack != "Not specified":  # Skip rows where the tech stack is "Not specified"
                repo_data.append({
                    'Repository Link': repo_url,
                    'Programming Language': primary_language,
                    'Tech Stack': tech_stack
                })
    
    return pd.DataFrame(repo_data)



def process_data(username, url, pdf_file_path, vecdbname):

    # loader = WebBaseLoader("https://jobs.dell.com/en/job/singapore/machine-learning-engineer/375/71445795440")
    loader = WebBaseLoader(url)
    page_data = loader.load().pop().page_content

    prompt_job = PromptTemplate.from_template(
        """
        {page_data}
        ### INSTRUCTION:
        Extract the job postings and return them in JSON format containing
        "Role", "Experience", "Skills" and "Description".
        No preamble.
        """
        

        
    )

    chain = prompt_job | llm_gemini
    job_response = chain.invoke(input={'page_data':page_data})

    json_parser = JsonOutputParser()
    json_job = json_parser.parse(job_response.content)

    # Example usage
    # username = 'Ganesamanian'  # Replace with the GitHub username
    df = get_github_repos(username)

    client = chromadb.PersistentClient(vecdbname)
    collection = client.get_or_create_collection(name = "my_collection")

    if not collection.count():
        for _, row in df.iterrows():
            collection.add(documents=f"{row['Programming Language']} {row['Tech Stack']}",
                        metadatas={"links":row["Repository Link"]},
                        ids=[str(uuid.uuid4())])
            
    links = collection.query(query_texts=json_job["Skills"], n_results=5).get('metadatas', [])


    # Specify the path to your PDF file
    # pdf_file_path = "Ganesamanian_Kolappan_Resume_.pdf"

    # Initialize the PyPDFLoader with the file path
    loader = PyPDFLoader(pdf_file_path)

    # Load documents from the PDF
    resume = loader.load()


    prompt_resume = PromptTemplate.from_template(
        """
        {resume_data}
        ### INSTRUCTION:
        Extract the resume content and return them in JSON format containing
        "Last Role", "Total Experience", "Skills", "Education", "project" and "Language".
        No preamble.
        """
        
    )

    chain = prompt_resume | llm_gemini
    response_resume = chain.invoke(input={'resume_data':resume})
    json_resume = json_parser.parse(response_resume.content)

    prompt_response = PromptTemplate.from_template(
         """
            {job_description}

            ### INSTRUCTION:
            Give how much the project from {link_list} and {profile} matches with the {job_description} in percentage.
            Provide the below
            1. profile Match percentage with the job as key "profileMatchPercentage",
            2. the project links related to the job description from the {link_list} as key "relatedprojectname",
            3. reume tips to improve the resume for the job as key "tipsToImproveResume",
            4. tips on how to write a cover letter for this job as key "tipsToWriteCoverLetter".
            in JSON format
            No PREAMBLE.
    
    """
        
    )

    chain = prompt_response | llm_gemini
    res = chain.invoke({"job_description":str(json_job),"profile":json_resume, "link_list": links})
    json_result = json_parser.parse(res.content)
    print(json_result)
    return (json_result['profileMatchPercentage'],
            json_result['relatedprojectname'],
            json_result['tipsToImproveResume'],
            json_result['tipsToWriteCoverLetter'])


if __name__ == '__main__':
    process_data("Ganesamanian",
                 "https://www.amazon.jobs/en/jobs/2684263/data-scientist-demand-forecasting",
                 "Ganesamanian_Kolappan_Resume_.pdf",
                 "vectorstoregit")