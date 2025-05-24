import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

st.set_page_config(page_title="Nice Classification Assistant", layout="wide")
st.title("Nice Classification Assistant")
st.write("Classify goods or services under the Nice system. Supports vague, ambiguous, and linguistically incorrect terms (TV, TC, TI).")

st.markdown("""
<style>
.answer-block {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    padding: 1rem;
    border-radius: 0.375rem;
    margin-bottom: 1.5rem;
    font-size: 1.05em;
    line-height: 1.6;
}
.main .block-container {
    max-width: 900px;
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

if not openai_api_key or not pinecone_api_key:
    st.error("Missing API keys.")
    st.stop()

try:
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=openai_api_key)

    vector_store_alpha = PineconeVectorStore(
        index_name="nice-alphabetical-list",
        embedding=embeddings,
        text_key="term",
        pinecone_api_key=pinecone_api_key
    )
    alpha_retriever = vector_store_alpha.as_retriever(search_kwargs={"k": 10})

    vector_store_ipos = PineconeVectorStore(
        index_name="nice-ipos-database",
        embedding=embeddings,
        text_key="term",
        pinecone_api_key=pinecone_api_key
    )
    ipos_retriever = vector_store_ipos.as_retriever(search_kwargs={"k": 10})

except Exception as e:
    st.error("Vector store error.")
    st.error(traceback.format_exc())
    st.stop()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key, temperature=0)

# Prompt with improved TC rule
prompt_template_str = """
You are an expert assistant specialized in the Nice Classification system. Your task is to classify goods or services — especially vague or problematic terms — using:

1. WIPO Alphabetical List (preferred)
2. IPOS Database (secondary)
3. WIPO classification logic (function, purpose, activity)

You must also handle general questions and apply official WIPO reasoning codes for problematic terms.

---

## Classification Logic:

- Determine if it's a good or service.
- Retrieve context from WIPO and IPOS.
- If both fail, apply classification principles.

---

## WIPO Problem Codes (Must apply strictly):

**TV - Too Vague**  
- Term is ambiguous or nonspecific.  
- Example: “chips”, “video games”, “cement”.

**TC - Linguistically Incorrect**  
- Spelling, grammar or structure error.  
- Always mark as TC even if the intended word is obvious.  
- Example: “childrens’ clothing” → “children’s clothing”, “computerz” → “computers”.

**TI - Incomprehensible**  
- Term has no clear meaning.  
- Example: “Spreadable maculature”.

If any of these apply, use this format:
<p><strong>Assessment</strong>: [TV/TC/TI] - [brief explanation and suggested corrected term]</p>

You may then classify the **corrected version**, if clear.

---

## Special Rule – Divergence in Sources:

If related terms retrieved are found in **multiple Nice classes**, and the ambiguity cannot be resolved, respond:
<p><strong>Assessment</strong>: TV - The term is too vague. It could refer to goods or services in multiple classes. Please specify the intended nature.</p>

---

## Response Format:

If valid:
<p><strong>Class</strong>: [Class]</p>
<p><strong>Explanation</strong>: [Justify using sources or principles]</p>

Always reply in fluent English with HTML formatting using <p> and <strong>.

---

Input: {question}

WIPO Context:
{alpha_list_context}

IPOS Context:
{ipos_database_context}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["alpha_list_context", "ipos_database_context", "question"],
    template=prompt_template_str
)

chain: RunnableSequence = prompt | llm | StrOutputParser()

with st.form(key="query_form"):
    query = st.text_input(
        "Enter a term or question:",
        placeholder="e.g., computerz, What is Class 42?",
        help="Enter a term to classify or a general question."
    )
    submitted = st.form_submit_button("Submit")

if submitted and query:
    with st.spinner("Processing..."):
        try:
            alpha_docs = alpha_retriever.invoke(query)
            ipos_docs = ipos_retriever.invoke(query)

            alpha_context = "\n\n".join([
                f"Term: {doc.page_content} (ID: {doc.metadata.get('basic_number', 'N/A')}, Class: {str(int(float(doc.metadata.get('class_number')))) if doc.metadata.get('class_number') else 'N/A'})"
                for doc in alpha_docs
            ]) if alpha_docs else "No terms found in WIPO."

            ipos_context = "\n\n".join([
                f"Term: {doc.page_content} (ID: {doc.metadata.get('ipos_id', 'N/A')}, Class: {str(int(float(doc.metadata.get('class_number')))) if doc.metadata.get('class_number') else 'N/A'}, Source: IPOS)"
                for doc in ipos_docs
            ]) if ipos_docs else "No terms found in IPOS."

            answer = chain.invoke({
                "alpha_list_context": alpha_context,
                "ipos_database_context": ipos_context,
                "question": query
            })

            st.subheader("Answer")
            st.markdown(f"<div class='answer-block'>{answer}</div>", unsafe_allow_html=True)

            st.subheader("Sources")

            st.markdown("**WIPO Alphabetical List:**")
            if alpha_docs:
                for doc in alpha_docs:
                    cls = doc.metadata.get("class_number")
                    basic_id = doc.metadata.get("basic_number", "N/A")
                    class_display = str(int(float(cls))) if cls else "Unknown"
                    st.markdown(f"- {doc.page_content} (ID: {basic_id}, Class: {class_display})")
            else:
                st.write("No terms retrieved from WIPO.")

            st.markdown("**IPOS Database:**")
            if ipos_docs:
                for doc in ipos_docs:
                    cls = doc.metadata.get("class_number")
                    ipos_id = doc.metadata.get("ipos_id", "N/A")
                    class_display = str(int(float(cls))) if cls else "Unknown"
                    st.markdown(f"- {doc.page_content} (ID: {ipos_id}, Class: {class_display}, Source: IPOS)")
            else:
                st.write("No terms retrieved from IPOS.")

        except Exception as e:
            st.error(f"Error: {e}")
            st.error(traceback.format_exc())
