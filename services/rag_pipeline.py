from crewai.tools import BaseTool
import chromadb
import uuid, json
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from services.scraper import Scraper
from services.scrapers.remoteok import RemoteOk
from utilities import convert_json_txt

class RAGPipeline(BaseTool):
    name: str = "rag_pipeline"
    description: str = "It will retrive jobs from filtered jobs folder and store embedded to vectordb chromadb"

    def _initialize_pipline(self, query, collection_name: str = "resume_retriever"):
        self._embedder = None
        self._scraper = Scraper(query, scrapers_list=[RemoteOk()])
        self._client = chromadb.Client()
        self._collection = self._client.get_or_create_collection(
            name=collection_name
        )

    def _document_loader(self, documents_path: str = "data/raw_jobs"):
        try:
            doc_dir = DirectoryLoader(
                path=documents_path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={
                    'encoding': 'utf-8'
                }
            )
            self._docs = doc_dir.load()
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _document_splitter(self):
        if not hasattr(self, "_docs") or not self._docs:
            raise ValueError("❌ No documents loaded. Check loader.")
        
        self._splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""]
        )
        self._chunks = self._splitter.split_documents(
            self._docs
        )
    
    def _document_embedder(self, query, model_name: str = "sentence-transformers/all-mpnet-base-v2") -> list:
        if not self._embedder:
            self._embedder = SentenceTransformer(model_name)
        
        return self._embedder.encode(query)
    
    def _add_document(self):
        ids = []
        metadatas = []
        embeddings = []

        for i, doc in enumerate(self._chunks):
            doc_id = f"doc-{uuid.uuid4().hex[:8]}-{i}"
            
            ids.append(doc_id)

            metadata = doc.metadata
            metadata["size"] = len(doc.page_content)
            metadata["doc_id"] = doc_id
            metadatas.append(metadata)

            embeddings.append(self._document_embedder(doc.page_content))
        
        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=[doc.page_content for doc in self._chunks],
            metadatas=metadatas
        )

    
    def _retrieve_doc(self, query: str = "", similarity_score: float = 0.0):
        query_embeddings = self._document_embedder([query]).tolist()

        results = self._collection.query(
            query_texts=[query],
            query_embeddings=query_embeddings,
            n_results=2
        )

        output = []
        if results and results['documents']:
            for i, doc in enumerate(results['documents']):
                distances = results['distances'][0][i]
                dis = (1 - distances if distances < 1 else distances - 1)
                if similarity_score < dis:
                    output.append(f"metadata: {convert_json_txt(results['metadatas'][0][i])}\ndocument: {results['documents'][0][i]}")
        
        return " ".join(output)

    def _generate_prompt(self, context, query):
        prompt = f"""
                You are a AI job assistent

                context: 
                {context}

                User query:
                {query}

                Return number of point based on factual information.
                The information should be based on the skill set which is mentioned in context and query.
                No special characters or symbols.
                Must provide information in number of points.
                """
        return prompt
    
    def _run(self, query: str):
        print("✅ NEW RAG RUNNING")
        self._initialize_pipline(query)
        self._document_loader()
        self._document_splitter()
        self._add_document()
        context = self._retrieve_doc(query)
        return self._generate_prompt(context, query)