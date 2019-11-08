ID = raw_input("Please type your ID: ")
PW = raw_input("Please type your PW: ")

with open("hello_world.txt", "w") as f:
    f.write("ID:"+ID+"\n")
    f.write("PW:"+PW+"\n")
    f.write("hello world\n")