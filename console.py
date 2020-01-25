#!/usr/bin/python3
import json
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    l_classes = ["BaseModel", "User", "Place", "State", "City",
                 "Amenity", "Review"]

    def default(self, line):
        args = line.split(".")
        all_objects = storage.all()
        if len(args) == 2:
            if args[1] == "all()":
                self.do_all(args[0])
            elif args[1] == "count()":
                count = 0
                for key in all_objects:
                    class_type = key.split(".")[0]
                    if class_type == args[0]:
                        count += 1
                print(count)
            elif args[1][0:5] == "show(":
                id = args[1].split("(")[1][:-1]
                self.do_show("{} {}".format(args[0], eval(id)))
            elif args[1][0:8] == "destroy(":
                id = args[1].split("(")[1][:-1]
                self.do_destroy("{} {}".format(args[0], eval(id)))
            elif args[1][0:7] == "update(":
                parameters = args[1].split("(")[1][:-1]
                id = parameters.split(", ")[0]
                variable = parameters.split(", ")[1]
                if variable[0] != "{":
                    value = parameters.split(", ")[2]
                    self.do_update("{} {} {} {}".format(args[0], eval(id),
                                                        eval(variable), value))
                else:
                    variable =  eval("{" + parameters.split(" {")[1])
                    for k, v in variable.items():
                        if type(v) is str:
                            v = '"' + v + '"'
                        print(v)
                        self.do_update("{} {} {} {}".format(args[0], eval(id),
                                                            k, v))


    def do_update(self, line):
        args = line.split(" ")
        all_objs = storage.all()
        if not line:
            print("** class name missing **")
        elif args[0] not in self.l_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in all_objs:
            print("** no instance found **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            if args[2] != "id" or args[2] != "created_at" or args[2] != "updated_at":
                key = "{}.{}".format(args[0], args[1])
                setattr(all_objs[key], args[2], eval(args[3]))
                storage.save()

    def do_create(self,arg):
        if not arg:
            print("** class name missing ** ")
        elif arg not in self.l_classes:
            print("** class doesn't exist **")
        else:
            new = eval(arg)()
            new.save()
            print(new.id)

    def do_show(self, line):
        args = line.split()
        if not line:
            print("** class name missing **")
        elif args[0] not in self.l_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            key = "{}.{}".format(args[0], args[1])
            if key in all_objs:
                print(all_objs[key])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        args = line.split()
        if not line:
            print("** class name missing **")
        elif args[0] not in self.l_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            key = "{}.{}".format(args[0], args[1])
            if key in all_objs:
                del all_objs[key]
                storage.all()
            else:
                print("** no instance found **")

    def do_all(self, line):
        args = line.split()
        list_ret = []
        all_objs = storage.all()
        if line == "":
            for k in all_objs:
                list_ret.append(str(all_objs[k]))
            print(list_ret)
        elif args[0] in self.l_classes:
            for k in all_objs:
                if k.split(".")[0] == args[0]:
                    list_ret.append(str(all_objs[k]))
            print(list_ret)
        else:
            print("** class doesn't exist **")

    def do_quit(self, arg):
        """stop comman line interpreter\n"""
        return True

    def do_EOF(self, arg):
        """stop comman line interpreter\n"""
        print()
        return True

    def emptyline(self):
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
