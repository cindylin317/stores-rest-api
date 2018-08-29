from flask_restful import Resource, reqparse

from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type =str,
        required=True,
        help='This field cannot be left blank')

    parser.add_argument('password',
        type =str,
        required=True,
        help='This field cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_name(data['username'])
        if user:
            return {"message":"The username has been used"},400
        else:
            user = UserModel(**data)
            user.save_to_db()
            return {"message": "user created sucessfully"}, 201

if __name__ == "__main__":
     myuser = UserModel.find_by_name("Cindy")
     if myuser:
         print("User: ID {}, name {}, password {}".format(myuser.id,
                          myuser.username, myuser.password))
     else:
         print(None)
