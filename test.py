# import PyMuPDF
#
# def extract_text_from_pdf_pymupdf(pdf_path):
#     text = ""
#     with PyMuPDF.open(pdf_path) as doc:
#         for page in doc:
#             text += page.get_text()
#     return text
#
# # Example usage
# pdf_file = "cv-test.pdf" # Replace with your PDF file name
# extracted_text = extract_text_from_pdf_pymupdf(pdf_file)
# print(extracted_text)

cv="""Voici un exemple de CV conçu pour correspondre parfaitement à l'offre d'emploi de Data Analyst chez PwC Technology Acceleration Center (TAC) en Tunisie. Ce modèle met en avant les compétences et l'expérience requises, en adoptant une structure claire et professionnelle.

[Prénom Nom]

[Adresse] | [Numéro de téléphone] | [Adresse e-mail] | [URL de votre profil LinkedIn]

Profil

Analyste de données avec [Nombre, ex: 3] ans d'expérience dans l'interprétation et l'analyse de données pour éclairer la prise de décision stratégique. Spécialisé dans la collecte, le nettoyage et la modélisation de données complexes, ainsi que dans la création de visualisations percutantes pour communiquer des informations clés. Passionné par la résolution de problèmes et désireux de contribuer à la transformation numérique au sein d'un environnement innovant comme le PwC TAC.

Expérience Professionnelle

Data Analyst | [Nom de l'entreprise précédente] | [Ville] | [Date de début] – [Date de fin]

Collecte et Nettoyage de Données : Mise en place et optimisation de processus pour collecter, nettoyer et organiser des ensembles de données volumineux provenant de sources multiples (SQL, CRM, ERP), garantissant une intégrité des données supérieure à 98%.

Analyse et Identification de Tendances : Réalisation d'analyses exploratoires et statistiques pour identifier des tendances, des modèles et des corrélations significatives, conduisant à une amélioration de [mentionner un résultat spécifique, ex: l'efficacité opérationnelle de 15%].

Reporting et Visualisation : Conception et développement de tableaux de bord interactifs et de rapports automatisés avec Power BI et Tableau, permettant aux parties prenantes de suivre les indicateurs de performance clés (KPIs) en temps réel.

Collaboration Inter-équipes : Travail en étroite collaboration avec les équipes marketing, financières et opérationnelles pour définir les besoins en analyse, traduire les exigences métier en spécifications techniques et présenter les résultats de manière claire et concise.

Amélioration Continue : Participation active à l'amélioration des pipelines de données et des méthodologies d'analyse, ce qui a permis de réduire le temps de traitement des données de 20%.

Data Analyst (Stagiaire/Junior) | [Nom de l'entreprise] | [Ville] | [Date de début] – [Date de fin]

Contribution à la maintenance des bases de données et à l'assurance qualité des données.

Assistance dans la préparation de rapports hebdomadaires et mensuels pour le management.

Analyse de données clients pour segmenter le marché et identifier de nouvelles opportunités.

Compétences Techniques

Analyse de Données : SQL (avancé), Python (Pandas, NumPy), R

Outils de Visualisation : Power BI (expert), Tableau (avancé)

Bases de Données : MySQL, PostgreSQL, Microsoft SQL Server

Cloud Computing : Connaissances de base sur AWS ou Microsoft Azure

Autres : Microsoft Excel (avancé, incluant les tableaux croisés dynamiques et Power Query), Git

Compétences Personnelles

Analyse et Résolution de Problèmes : Solide capacité à décomposer des problèmes complexes et à proposer des solutions basées sur les données.

Communication : Excellentes compétences en communication orale et écrite, capable de vulgariser des informations techniques pour un public non expert.

Esprit d'Équipe : Aptitude confirmée à collaborer efficacement avec des équipes pluridisciplinaires.

Rigueur et Organisation : Souci du détail et capacité à gérer plusieurs projets simultanément tout en respectant les délais.

Formation

[Nom du diplôme, ex: Mastère Professionnel en Statistique et Analyse de l'Information] | [Nom de l'université] | [Ville] | [Année d'obtention]

[Nom du diplôme, ex: Licence en Informatique de Gestion] | [Nom de l'université] | [Ville] | [Année d'obtention]

Langues

Français : Langue maternelle

Anglais : Courant (Niveau C1) - Requis pour le poste

Arabe : Langue maternelle

Centres d'Intérêt

Veille technologique sur l'intelligence artificielle et le machine learning.

Participation à des compétitions de data science (ex: Kaggle).

[Autre intérêt pertinent, si applicable]."""
from openai import OpenAI  # Or your preferred LLM library
import datetime

current_date = str(datetime.datetime.now())

cv_extraction_prompt="""You are a seasoned Principal Engineer acting as a hiring manager. Your task is to review a candidate's resume and distill their experience into a structured JSON object for an internal recruiting tool. Your primary goal is to identify their most significant and demonstrated technical skills and calculate their total experience.

You will be given the current date to accurately calculate experience for roles listed as "Present".

Your response must be ONLY the valid JSON object.

---
### **JSON SCHEMA, Instructions AND GUIDELINES**

{
  "match_context": "string",
  "hard_skills": ["string"],
  "domain_keywords": ["string"],
  "job_title": "string",
  "total_years_of_experience": "integer | null"
}

*   **`match_context`**:
    *   In your own words as an engineer, write a brief, 3-4 sentence summary of the candidate's professional profile.
    *   **Focus on their core actions and business outcomes** (e.g., 'specializes in building scalable backend services,' 'proven experience in cloud infrastructure migration').
    *   **Do not list specific technologies or tools in this summary.**

*   **`hard_skills`**:
    *   As a hiring manager, identify all technical hard skills demonstrated by the candidate.
    *   Scan the entire resume, including summaries, skill sections, and work experience descriptions.
    *   **CRITICAL FORMATTING RULE:** The final list must contain **ONLY the technology name itself.** For example, if the text says "Experience with Python", the value in the list must be `"Python"`, not `"Experience with Python"`.

*   **`domain_keywords`**:
    *   List the key business or process-related terms that define the candidate's experience (e.g., "SaaS", "FinTech", "Agile", "CI/CD", "Data Governance").

*   **`job_title`**:
    *   Extract the candidate's most recent or current job title.

*   **`total_years_of_experience`**:
    *   Calculate the candidate's total years of professional experience as an integer.
    *   Parse the start and end dates from their work history.
    *   Use the provided **Current Date** as the end date for any role listed as "Present" or without an end date.
    *   Sum the duration of all roles. Round the final number to the nearest whole integer.
    *   If no work history or dates are provided, return null.

ABSOLUTELY CRITICAL - READ THIS CAREFULLY:
1. NO markdown formatting whatsoever
2. NO ```json or ``` in your response
3. Start with "{{" and end with "}}"
---

### **BEGIN REVIEW**

Review the following resume text and produce the JSON object.

**Current Date:**"""+current_date+'\n**Resume Text:**'
import re
import json
from sentence_transformers import SentenceTransformer
import torch
MODEL_NAME = 'all-MiniLM-L6-v2'

client = OpenAI(base_url="https://api.llm7.io/v1",api_key="4LPcl/IAgbPijsDc3iQXFSSYy9Mb1Xj1ieIZnRb1ZDtzNDW0Kmwisz7mphyed3oN+srfcqMqx2PnbOc19cvE0TgJE02HeZgndZPxUU5haEVpOCKj0Fq3xTrUZaSirYgxUSE=")
try:
    response = client.chat.completions.create(
        model="gemini-2.5-pro", # Use a model that's good at following JSON instructions
        messages=[
            {"role": "user", "content": cv_extraction_prompt + cv}
        ],
        response_format={"type": "json_object"} # Enforce JSON output
    )
    content = response.choices[0].message.content
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        match_content=json.loads(match.group(0))["match_context"]
    else:
        print("error")
except Exception as e:
    # Catching any exception during the API call or parsing
    print(f"A single request failed with error: {e}")


device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

print(f"Loading multilingual embedding model: {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME, device=device)
print("Model loaded successfully.")
MODEL_NAME = 'all-MiniLM-L6-v2'
BATCH_SIZE=32
all_embeddings = model.encode(
    match_content,
    batch_size=BATCH_SIZE,
    show_progress_bar=True,
    normalize_embeddings=True # Normalizing is essential for accurate cosine similarity.
)
