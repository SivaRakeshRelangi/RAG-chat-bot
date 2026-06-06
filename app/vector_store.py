import faiss
import numpy as np

class VectorStore:

    def __init__(self, dim):

        quantizer = faiss.IndexFlatIP(dim)

        self.index = faiss.IndexIVFFlat(
            quantizer,
            dim,
            100,
            faiss.METRIC_INNER_PRODUCT
        )

        self.metadata = []
        self.trained = False