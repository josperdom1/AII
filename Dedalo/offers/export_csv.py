from offers.models import Offer


def extract_offers():
    offers = Offer.objects.all()
    
    for o in offers:
        print(str(o))
        
        

