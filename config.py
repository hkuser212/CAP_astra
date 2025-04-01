# import os
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.schema import HumanMessage
# from langchain_ollama import ChatOllama
# from langchain.docstore.document import Document
# from PyPDF2 import PdfReader

# # Ensure embeddings are updated to match LangChain updates
# embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# ollama_model = ChatOllama(model="llama3:latest", base_url="http://localhost:11434")

# def extract_text_from_pdf(pdf_file):
#     print("Extracting text from the PDF...")
#     text = ""
    
#     try:
#         with open(pdf_file, 'rb') as file:
#             pdf_reader = PdfReader(file)
            

#             for page in pdf_reader.pages:
#                 text += page.extract_text()
                
#         print("PDF text extraction completed.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
    
#     return text

# def get_text_chunks(text):
#     print("Splitting text into smaller chunks...")
#     text_splitter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size=200,
#         chunk_overlap=40,
#         length_function=len,
#     )
#     chunks = text_splitter.split_text(text)
#     print("Text splitting completed.")
#     return chunks

# def database(chunks):
#     print("Creating vector store from text chunks...")
#     vector_store = FAISS.from_texts(texts=chunks, embedding=embedding_model)
#     print("Vector store creation completed.")
#     return vector_store

# def conversational_retrieval_with_ollama(vector_store, query):
#     print("Performing similarity search on the vector store...")
#     docs = vector_store.similarity_search(query, k=2)
    
#     if not docs:
#         print("No relevant content found in the PDF. Falling back to general knowledge.")
#         prompt = f"The following query is unrelated to the provided document:\n\n{query}"
#     else:
#         print(f"Found {len(docs)} relevant documents.")
#         context = "\n".join([doc.page_content for doc in docs])
#         print("\n--- Retrieved Context ---")
#         print(context)
#         prompt = f"The following context is provided, If there is any calculation work in general required then calculate and present the answer:\n{context}\n\n{query}"

#     print("\n--- Generated Prompt ---")
#     print(prompt)

#     print("Querying Ollama model with the prompt...")
#     response = ollama_model([HumanMessage(content=prompt)])  # Correct interface
#     print("Received response from Ollama model.")
#     return response.content


# def main(pdf_file, query):
#     print("Starting main function...")
#     text = extract_text_from_pdf(pdf_file)
#     chunks = get_text_chunks(text)
#     vector_store = database(chunks)
#     response = conversational_retrieval_with_ollama(vector_store, query)
#     print("Main function execution completed.")
#     return response


# def input(pdf_file,query):
#     # pdf_file = "ss.pdf"  # User's specified PDF file
#     # query = "Who is author of book monk who sold his ferrari?"

#     try:
#             response = main(pdf_file, query)
#             print("Response from the Ollama model:")
#             print(response)
#             return response
#     except Exception as e:
#             print("An error occurred:")
#             print(str(e))