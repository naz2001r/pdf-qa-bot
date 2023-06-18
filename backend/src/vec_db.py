import os
import pickle
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

class VectorizeDB:
    """
        A class for vectorizing datasets.
    """
    def __init__(self, openai_key=""):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
        self.__db = None
        self.__retriver = None

    def vectorize(self, pages:list, extend=False) -> None:
        if self.__db is not None and extend:
            db_new = FAISS.from_documents(pages, self.embeddings)
            self.__db = self.__db.merge_from(db_new)

        else:
            self.__db = FAISS.from_documents(pages, self.embeddings)
    
    @property
    def retriver(self) -> object:
        return self.__retriver
    
    @retriver.setter
    def retriver(self, k:int = 5) -> None:
        if not isinstance(k, int):
            raise TypeError(f"Type {type(k)} is not suported for number of query output `k`")
        self.__retriver = self.__db.as_retriever(search_kwargs={"k": k})

    def query(self, text:str) -> list:
        if self.retriver:
            return self.retriver.get_relevant_documents(text)
        raise TypeError('Please set retriver before calling it.')
    
    @classmethod
    def load_db(cls, file_name: str) -> object:
        return pickle.load(open(file_name, 'rb'))
    
    def dump_db(self, file_name: str) -> None:
        pickle.dump(self, open(file_name, 'wb'))