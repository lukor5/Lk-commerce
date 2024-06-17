def obfuscate_card_number(card_number):
    if len(card_number) < 16:
        raise ValueError("Card number too short to obfuscate properly.")
    
    length = 4
    obfuscated_group = '*' * length
    
    formatted_card_number = ' '.join([
        card_number[:length],   
        obfuscated_group,
        obfuscated_group,              
        card_number[-length:]  
    ])
    return formatted_card_number