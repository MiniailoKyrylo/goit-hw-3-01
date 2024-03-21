import pickle
import os

"""Class for serializing and deserializing the address book."""
class Serializer:

    """
    Attributes:
    - contacts (list): Stores the list of contacts 
    - path (str): Stores the path to the address book file
    """

    # Serialization
    @staticmethod
    def _serialize_dict(contacts: list, path: str):
        """Serialize the dictionary."""
        try:
            with open(path, 'wb') as file:
                pickle.dump(contacts, file)
        except Exception as e:
            raise Exception(f'Serializer - Error during serialization of the dictionary: {e}')

    # Deserialization
    @staticmethod
    def _deserialize_dict(path):
        """Deserialize the dictionary."""
        if not os.path.exists(path) or not os.path.getsize(path) > 0:
            return []
        
        try:
            if os.path.exists(path) and os.path.getsize(path) > 0:
                with open(path, 'rb') as file:
                    a = pickle.load(file)
                    return a
        except Exception as e:
            raise Exception(f'Serializer - Error during deserialization of the dictionary: {e}')