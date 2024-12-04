import os

import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI
from pprint import pprint
import json
from test import new_df


load_dotenv()

AZUR_ENDPOINT = os.getenv("AZUR_ENDPOINT")
AZUR_KEY = os.getenv("AZUR_KEY")


df = pd.read_csv("postgres_data/france_travail_clean.csv")
print(df.shape)



client = AzureOpenAI(
    api_key="DHEM1xz6J2UQGOhfuI1M8mwcb6yuyBCzNwuOYjvn19q9CPl6gZgOJQQJ99AKAC5RqLJXJ3w3AAABACOGYLdQ",  
    api_version="2024-10-21",
    azure_endpoint="https://openaishuto.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview"
    )

deployment_name="gpt-35-turbo (version:0301)"


all_job_description = df[["id", "description"]].iloc[:3]



prompt =\
"""
Ta tâche est d'extraire toutes les compétences mentionnées dans une offres d'emploi. Ton objectif est d'extraire et de catégoriser ces compétences sous format json.
Extrait les compétences selon le schéma suivant: {index: [category1: [compétence1, compétence2, compétence3, etc.], category2: [compétence4, compétence5, compétence6, etc.]]}.
Assume everything mentioned refers to the same thing. 
The extracted information should be categorized according to the allowed categories specified below.

Constraints:
  - Allowed Categories: "Hard skill", "Soft skill", "Technologie"
 
"""
prompt += f"Input: {all_job_description}"
prompt += "\nOutput:"



for job in all_job_description:
    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "assistant",
                "content": prompt,
            },
        ],
    )


response = completion.choices[0].message.content

data = json.loads(response)

skill_df= pd.DataFrame(data)

transposed_skill_df = skill_df.T       #invert index & column names (T = transpose)

indexReset_df = transposed_skill_df.reset_index()  #assign "id" as a column as it previously got assigned to the skill_df's index

cleaned_skills_df = indexReset_df.rename(columns={"index": "id",
                     "Hard skill" : "competences",
                       "Soft skill": "qualitesProfessionnelles",
                         "Technologie" : "formations"},)


new_df["competences"].iloc[:3] = cleaned_skills_df["competences"]
new_df["qualitesProfessionnelles"].iloc[:3] = cleaned_skills_df["qualitesProfessionnelles"]
new_df["formations"].iloc[:3] = cleaned_skills_df["formations"]

print(new_df.iloc[:3])
