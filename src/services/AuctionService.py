# import datetime
# from sqlalchemy.orm import Session
# from models.Auction import Auction

# session = Session()

# auction1 = Auction('Ferrari', 250, 'Sedan', datetime.datetime.utcnow)

# def create(obj):
#     try:
#         session.add(obj)
#         session.commit()
#         session.close()
#     except:
#         "Não"

# if __name__ == '__main__':
#     create(auction1)