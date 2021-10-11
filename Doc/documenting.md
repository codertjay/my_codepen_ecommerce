The models of this project is going to have

Customer Model:
    user = OnetoOneField( to django dafault user)
    name = Charfield
    email = Charfield
    

Product Models:
    name = charfield (product name)
    price = decimalfield()
    digital = BooleanField(default = False)
    image = Imagefield
    
    
    
Order Models:
    customer= Foreignkey(many to one rel to the customer)
    datetime field = autho now add
    complete = Booleanfield(default = false check if ordered)
    transaction_id = Charfield()
    
    
    return transaction id
  
  
    
Order_item Models :
    product = Foreignkey(many to one rel to the product)
    order = Foreignkey (many to one rel to the Order)
    quantity = integerfield
    date_added = Datetimefield
    
    
    
    
Shipping models:
    customer = Foreignkey(Customer)
    order = Foreignkey(Order)
    address = Charfield
    city = Charfield
    state = charfield
    zipcode = Charfield
    date_added = Datetimefield autu now add
    
    return address
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     