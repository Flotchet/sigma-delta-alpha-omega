import sqlalchemy
import hashlib
import string 




def create_user(username, password, password2, conn) :
    
        #check if the user exists
        if conn.execute(sqlalchemy.text(f"""SELECT EXISTS(SELECT 1 FROM users WHERE username = '{username}')""")).fetchone()[0]:
            return "User already exists"

        #check the password
        if password != password2:
            return "Passwords don't match"
        
        #check the password length 
        if len(password) < 10:
            return "Password too short"
        
        #check the password for special characters, numbers and letters
        if not any(char in string.punctuation for char in password):
            return "Password must contain special characters"
        

        if not any(char.isdigit() for char in password):
            return "Password must contain numbers"
        

        if not any(char.isalpha() for char in password):
            return "Password must contain letters"
            
        #check the username length
        if len(username) < 5:
            return "Username too short"
        
        #put the user in the database
        conn.execute(sqlalchemy.text(f"""INSERT INTO users (username, password, attr_level) VALUES ('{username}', '{hashlib.sha256(password.encode()).hexdigest()}', 1)"""))
        
        return """<meta http-equiv="refresh" content="0; URL=/login" />"""
            
        
