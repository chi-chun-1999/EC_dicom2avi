import hashlib
import abc


class EncryptAbstract(abc.ABC):
    def __init__(self) -> None:
        self._encrypt_data = None
        pass

    @abc.abstractmethod
    def encrypt(self,text):
        pass

class SHAEncrypt(EncryptAbstract):
    def __init__(self,length=10) -> None:
        super().__init__()
        self._encrypt_length = length
    
    def encrypt(self,text):
        sha1 = hashlib.sha1()
        sha1.update(text.encode('utf-8'))
        self._encrypt_data = sha1.hexdigest()
        if len(self._encrypt_data)<self._encrypt_length:
            return self._encrypt_data
        else:
            return self._encrypt_data[:self._encrypt_length]
        
        