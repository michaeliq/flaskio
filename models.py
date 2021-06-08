from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, DateTime
from app import db

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

class Room(db.Model):
     __tablename__ = "room"
     _id = Column(Integer, primary_key=True)
     name = Column(String(35),nullable=False)
     created_at = Column(DateTime,nullable=False)
     created_by = Column(String(35),nullable=False)

class RoomMember(db.Model):
     __tablename__='room_members'
     _id = Column(String(50), primary_key=True)
     room_name = Column(String(25), nullable= False)
     is_room_admin = Column(Boolean, nullable=False)
     added_at=Column(DateTime, nullable=False)
     added_by = Column(String(25),nullable=False)

class User(db.Model):
     __tablename__= "users"
     user_id = Column(String(50), primary_key=True)
     username = Column(String(30), nullbale=False)
     password = Column(String(300), nullable=False)

def get_room(room_id):
     if room_id:
          room = Room.query.get(room_id)
          return room


def get_room_members(room_id):
     if room_id:
          members = RoomMember.query.filter_by(_id=room_id)
          return members

def is_room_member(user_id,room_id):
     if user_id and room_id:
          if RoomMember.query.filter_by(_id=room_id + "," +user_id):
               return True
          else:
               return False

def is_room_admin(user_id,room_id):
     if user_id and room_id:
          user = RoomMember.query.get(user_id)
          if room_id == user._id.split(',')[0]:
               return True

def update_room():
     pass

def remove_room_members():
     pass

def add_room_members():
     pass

def get_room_for_member(user_id):
     if user_id:
          rooms = RoomMember.query.all()
          member_rooms = [room for room in rooms if room._id.split(',')[1] == user_id]
          if len(member_rooms) > 0:
               return member_rooms


def save_room():
     pass

def delete_room():
     pass
