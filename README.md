# Natural Language Processing Project 

## About the Project
Natural Language Processing (NLP) uses programming and machine learning techniques to help understand and make use of large amounts of text data.

For this project, I will be scraping data from GitHub repository README files from some of the most starred repositories in order to build a model that can predict what programming language a repository is, given the text of the README file.

****

### Objectives for this project:
- Building a dataset based on a list of GitHub repositories to scrape, and writing the python code necessary to extract the text of the README file for each page, and the primary language of the repository.
- Documenting process and analysis throughout the data science pipeline.
- Constructing a classification model that can predict what programming language a repository is in, given the text of the README file.
- Deliverables:
    - A well-documented jupyter notebook that contains my analysis.

**** 

### Initial hypotheses
- What are the most frequently occuring words in most starred READMEs?
- Are there any words that uniquely identify a programming language?
- What are the top word combinations (bigrams and trigrams)?

****

### Data Dictionary

Feature      | Description   | Data Type
------------ | ------------- | ------------
repo | GitHub repositories webpage | object 
clean_content | Cleaned text from README files of GitHub repositories | object
language | Programming language used in README files of GitHub repositories | object 
 
****

### Pipeline Process:

#### Plan
- Understand project description and goals. 
- Form hypotheses and brainstorm ideas.
- Have all necessary imports ready for project.

#### 1. Acquire
- Scrape the README files from most starred Github repositories.
- Functions to acquire the data are included in [acquire.py](https://github.com/gabrielatijerina/nlp-project/blob/main/acquire.py).


#### 2. Prepare
- Normalize text, clean, tokenize, lemmatize and remove stopwords.
- Split the data into train, validate, test.
- Functions to prepare the data are included in [prepare.py](https://github.com/gabrielatijerina/nlp-project/blob/main/prepare.py).

#### 3. Explore
- Address questions posed in planning and brainstorming
- Produce bigrams, trigrams, and word clouds. 
- Create data visualizations
- Summarize key findings and takeaways

#### 4. Model/Evaluate
- Establish and evaluate a baseline model.
- Generate various classification algorithms and settle on the best algorithm by comparing evaluation metrics.
- Choose the best model and test that final model on out-of-sample data.
- Summarize performance, interpret, and document results.

#### 5. Deliver
- A final Jupyter Notebook [(Final-Notebook.ipynb)](https://github.com/gabrielatijerina/nlp-project/blob/main/final-notebook.ipynb) 

****
### Next Steps
- Gather higher quantity of READMEs from most starred GitHub repositories.
- Run statistical testing.
- Conduct more modeling.

****

### Recreating Project
- To reproduce this project, download [acquire.py](https://github.com/gabrielatijerina/nlp-project/blob/main/prepare.py), [prepare.py](https://github.com/gabrielatijerina/nlp-project/blob/main/prepare.py), and [final-notebook.ipynb](https://github.com/gabrielatijerina/nlp-project/blob/main/final-notebook.ipynb) in your working directory and follow the steps from the pipeline process above.
- Do any additional exploring, modeling, and evaluating of your own to deliver any new information