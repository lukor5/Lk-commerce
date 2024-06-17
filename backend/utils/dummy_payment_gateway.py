def process_payment(amount, card_number, expiry_date, cvv):
    if len(card_number) == 16 and expiry_date and cvv:
        if card_number == "4444333322221111":
            return True, "Payment successful", None  
        else:
            return False, "Payment declined", 'Card declined by bank'  
    return False, "Invalid payment details", 'Invalid card data'