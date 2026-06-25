from utils import dbconn, crypto
from core import session
from models.vault_entry import VaultEntry


def encrypt_and_save(title, username, password)-> bool:
    
    if session.KEY:
        
        ciphertext = crypto.encrypt_data(session.KEY, title, username, password)
        response = dbconn.save_entry(title, ciphertext)
        return response
    else:
        return None
    


def get_and_decrypt() -> list[VaultEntry]:
    view_bag = []

    if session.KEY:
        
        entries = dbconn.get_entries()
        if entries is None:
            return view_bag
        
        
        for entry in entries:
            entry_id = entry[0]
            entry_title = entry[1] 
            entry_bytes = entry[2]

            json_dictionary = crypto.decrypt_data(session.KEY, entry_bytes, entry_title)

            item = VaultEntry(
                id = entry_id,
                title = entry_title,
                username = json_dictionary["username"],
                password = json_dictionary["password"]
            )
            view_bag.append(item)
            
    return view_bag