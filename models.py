from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app import db
import bcrypt 

#Room Schema database
#Room
#    id, name, created_at, created_by
#Room Members
#    id[room,id_username],room_name,is_room_admin,added_at,added_by
#
#Room Operations
#
#Create Room
#    input: room_id
#    DB operations: is_room_member, get_room_members, get_room
#Edit Room
#    input:room_id,room_name,member
#    DB operations: get_room,get_room_members,is_room_admin,update_room,add_room_members,remove_room_members
#View Room
#    input: room_id
#    DB operations: is_room_member,get_room,get_room_members
#Homepage
#    get_room_for_members

salt = bcrypt.gensalt(12)

class Room(db.Model):
     __tablename__ = "room"
     _id = Column(String(100), primary_key=True, autoincrement=False)
     members = relationship('RoomMember')
     name = Column(String(35),nullable=False)
     created_at = Column(DateTime,nullable=False)
     created_by = Column(String(35),nullable=False)
     owner_room = Column(String(35),nullable=True)

class RoomMember(db.Model):
     __tablename__='room_members'
     _id = Column(String(100), primary_key=True, autoincrement=False)
     room_id = Column(String(100), ForeignKey("room._id"))
     user_id = Column(String(100), ForeignKey("users.user_id"))
     room_name = Column(String(25), nullable= False)
     is_room_admin = Column(Boolean, nullable=False)
     added_at=Column(DateTime, nullable=False)
     added_by = Column(String(25),nullable=False)

class User(db.Model):
     __tablename__= "users"
     user_id = Column(String(100), primary_key=True, autoincrement=False)
     rooms = relationship('RoomMember')
     username = Column(String(30), nullable=False)
     password = Column(String(300), nullable=False)
     location = Column(String(50), nullable=True, default="not defined")

     # problemas con la clave primaria, sqlite no permite usar una campo primario diferente 
     # de integer ya que internamente este se autoincrementa y al no poder ejecutar la operación aritmetica arroja un IntegrityError. Busco solución.
     # --Solución
     # se colocó autoincrement=False para desactivar el incremento automatico en el campo primario. 
     # 
     # Falta solucionar problema de alembic para las migraciones.
     # -- Solcionado
     # Alembic sigue generando una instrucción que borra una tabla inexistente en el
     # sistema, sin embargo se puede eliminar dicha instrucción, debe tomarse en cuenta esto
     # luego de ejecutar el comando fask db migrate para evitar errores durante el 
     # upgrade o downgrade

     def save_user(self):
          self.user_id=bcrypt.hashpw(self.username.encode(),salt).decode()
          self.password = bcrypt.hashpw(self.password.encode(),salt).decode()
          db.session.add(self)
          db.session.commit()

     def delete_user(self,_id):
          if _id:
               user = self.query.get(_id)
               if user: 
                    user.delte()
                    db.session.commit()
                    return _id
          return False

     def update_name(self,_id,new_name):
          if _id:
               user = self.query.get(_id)
               if user:
                    user.username = new_name
                    db.session.commit()
          return False
          

def get_room_members(room_id):
     if room_id:
          members = RoomMember.query.filter_by(_id=room_id)
          return members

def is_room_member(user_id,room_id):
     room = RoomMember.query.filter_by(room_id=room_id,user_id=user_id).first()
     if room:
          return True
     return False

def is_room_admin(user_id,room_id):
     room = RoomMember.query.filter_by(room_id=room_id,user_id=user_id).first()
     if room.is_admin_room:
          return True
     return False


def remove_room_members(users_id):
     for user_id in users_id:
          RoomMember.query.filter_by(user_id=user_id).delete()
     db.session.commit()

def add_room_members(users):
     for user in users:
          id = bcrypt(users[user].room_name.encode(),salt)
          new_member = RoomMember(
               _id=id,
               user_id = users[user].user_id,
               room_id= users[user].room_id,
               name=users[user].room_name,
               added_by=users[user].owner,
               added_at=datetime.now(),
               is_room_admin=users[user].is_admin)
          db.session.add(new_member)
     db.session.commit()


def save_room(room_name,created_by):
     id = bcrypt.hashpw(room_name.encode(),salt)
     user = User.query.get(created_by)
     new_room = Room(
          _id=id,
          name=room_name,
          created_by=user.username,
          created_at=datetime.now(),
          owner_room=created_by)
     db.session.add(new_room)
     db.session.commit()
     users = {[{"room_id":id,"user_id":user.user_id,"room_name":room_name,"owner":created_by,"is_admin":True}]}
     add_room_members(users)

def delete_room(room_id):
     Room.query.filter_by(_id=room_id).delete()
     db.session.commit()

def update_room(id_room,new_room_name,new_owner):
     update_room = Room.query.filter_by(_id=id_room)
     update_room.name = new_room_name
     update_room.owner_room = new_owner
     db.session.commit()

def get_room(room_name):
     if room_name:
          rooms = Room.query.filter_by(name=room_name)
          return rooms
