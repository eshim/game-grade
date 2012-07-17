import re

def get_pattern(s):
    if s == "(([A-Z_][A-Z1-9_]*)|(__.*__))"or s=="(([A-Z_][A-Z0-9_]*)|(__.*__))":
        return ("Your variable is a constant.\n" + 
                "Constants should be in ALL_CAPS.\n"+
                "A special case of constants have __two_underscores__ on either end.\n" +
                "Constants should use under_scores, not camelCase.\n" +
                "Constants should start with a letter, but can contain numbers.\n")
    elif s == "[a-z_][a-z1-9_]{2,30}$"or s=="[a-z_][a-z0-9_]{2,30}$":
        return ("Your variable is a function name.\n" + 
                "Functions should be in all_lowercase.\n" +
                "Functions should use under_scores, not camelCase.\n" +
                "Functions should be at least 2 characters long and no more than 30.\n" +
                "Functions should start with a letter, but can contain numbers.\n")
    elif s=="[a-z_][a-z0-9_]{2,30}$":
        return ("Your variable is a basic variable.\n" +
                "Basic variables should be in all_lowercase.\n" +
                "Basic variables should use under_scores, not camelCase.\n" +
                "Basic variables should be at least 2 characters long and no more than 30.\n" +
                "Basic variables should start with a letter, but can contain numbers.\n")
    elif s == "[A-Z_][a-zA-Z0-9]+" or s=="[A-Z_][a-zA-Z1-9]+":
        return ("Your variable is a class name.\n" +
                "Class names should use camelCase, not under_scores.\n" +
                "Class names should start with a Capital letter.\n" + 
                "Class names can contain lowercase and numbers.\n")
    elif s == "[A-Za-z_][A-Za-z0-9_]*" or s=="[A-Za-z_][A-Za-z1-9_]*":
        return ("Your variable is an inline variable, probably used in a generator.\n" +
                "Inline variables should use under_scores, not camelCase.\n" +
                "Inline variables should start with a Capital.\n" +
                "Inline variables can contain lowercase and numbers.\n")

def readable_output(output_file):
    try:
        fin = open(output_file)
    except:
        print "I think that file doesn't exist. At least, you did something wrong."
    else:
        output = ""

        for n in fin:
            output += n

        pretty_output = ""
        OPS = "([!][=]|[<][=]|[=][=]|[>][=]|[<]|[>]|[=]|[+][=]|[-][=]|[*][=]|[/][=]|[%])"
        DIG = "(\d*)([,]\d*)([:].*[:]|[:])"

        #Black listed names (C0102)
        if re.search(r'Black listed name', output):
            names = re.findall(r'%s( Black listed name )(.*)'%DIG, output)
            for n in names:
                pretty_output += ("The variable name you have used on line %s (%s) is reserved in Python.\n"%(n[0],n[4]) +
                                  "Choose a new name and be sure to change all instances of the variable.\n\n")

        #Invalid name format (C0103)
#        if re.search(r'Invalid name .* [(]should match', output):
#            names = re.findall(r'%s( Invalid name )(.*)( [(]should match )(.*)([)])'%DIG, output)
#            for n in names:
#                pretty_output += "Your variable name, %s (line %s) is formatted improperly.\n"%(n[4],n[0])
#                pretty_output += get_pattern(n[6]) + "\n"

        #Line too long (C0301)
        if re.search(r'Line too long', output):
            names = re.findall(r'%s( Line too long [(])(\d*)([/]\d*[)])'%DIG, output)

            for n in names:
                pretty_output += ("Line %s is too long.\n"%n[0] +
                                  "The maximum line length is 80 characters, but this line is %s characters.\n"%n[4] +
                                  "You can use parentheses to group items with a new item or part of an item on a single line.\n\n")

        #Module too long (C0302)
        if re.search(r'Too many lines in module', output):
            names = re.findall(r'%s( Too many lines in module [(])(.*)([)])'%DIG, output)

            for n in names:
                pretty_output += ("Module %s (line %s) has too many lines.\n"%(n[4], n[0]) +
                                  "You should try to separate the module into smaller pieces with more modules or functions.\n\n")

        #Multiple statements on a line (C0321)
        if re.search('More than one statement on a single line', output):
            lines = re.findall(r'%s( More than one statement on a single line'%DIG, output)

            for l in lines:
                pretty_output += ("On line %s you have more than one statement.\n"%l[0] +
                                  "You can only have one statement on a single line.\n\n")

        #Operator not preceded by space (C0322)
        if re.search(r'Operator not preceded by a space\n', output):
            lines = re.findall(r'%s( Operator not preceded by a space\n)(.*)%s(.*)'%(DIG,OPS), output)

            for l in lines:
                pretty_output += "On line %s, the operator \"%s\" needs a space before it.\n\n"%(l[0],l[5])


        #Operator not followed by space (C0323)
        if re.search('Operator not followed by a space', output):
            lines = re.findall(r'%s( Operator not followed by a space\n)(.*)%s(.*)'%(DIG,OPS), output)

            for l in lines:
                pretty_output += "On line %s, the operator \"%s\" needs a space after it.\n\n"%(l[0],l[5])

        #Comma not followed by space (C0324)
        if re.search('Comma not followed by a space', output):
            lines = re.findall(r'%s( Comma not followed by a space)'%DIG, output)

            for l in lines:
                pretty_output += "On line %s, the comma needs a space after it.\n\n"%l[0]

        #Unrecognized file option (E0011)
        if re.search('Unrecognized file option', output):
            names = re.findall(r'%s( Unrecognized file option )(.*)'%DIG, output)

            for n in names:
                pretty_output += "The option %s (line %s) is unrecognized.\n\n"%(n[4],n[0])

        #Bad option (E0012)
        if re.search('Bad option value', output):
            names = re.findall(r'%s( Bad option value )(.*)'%DIG, output)

            for n in names:
                pretty_output += "The option %s (line %s) is not a valid option.\n\n"%(n[4],n[0])

        #__init__ is generator (E0100)
        if re.search('__init__ method is a generator', output):
            names = re.findall(r'%s( __init__ method is a generator )'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you defined the __init__ method as a generator.\n"%n[0] +
                                  "The __init__ method is a special class method which should not include any generators.\n" +
                                  "Instead, separate the generator into a separate method and call it inside of __init__.\n\n")

        #Explicit return in __init__ (E0101)
        if re.search('Explicit return in __init__', output):
            names = re.findall(r'%s( Explicit return in __init__)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you included a return statement in the __init__ method.\n" +
                                  "The __init__ method is a special class method which should not return anything.\n" +
                                  "Instead, only assign values within the class object.\n\n")

        #Function, class, or method defined twice (E0102)
        if re.search(' already defined line ', output):
            names = re.findall(r'%s(.*)( already defined line )(.*)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you named a function, class, or method \"%s\".\n"%(n[0],n[3]) +
                                  "Unfortunately you already used that name on line %s.\n\n"%(n[5]) +
                                  "Rename one of them and be sure to change the name every time you call it.")

        #Loop keyword used outside of loop (E0103)
        if re.search('not properly in loop', output):
            names = re.findall(r'%s( .*)( not properly in loop)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you used the loop keyword %s\n"%(n[0],n[3]) +
                                  "However, this was not inside of a loop.\n" +
                                  "Check your indentation if you thought it was.\n\n")

        #Return outside function (E0104)
        if re.search('Return outside function', output):
            names = re.findall(r'%s( Return outside function'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you used the function keyword \"return\".\n"%n[0] +
                                  "However, this was not inside of a function.\n" +
                                  "Check your indentation if you thought it was.\n\n")

        #Yield outside function (E0105)
        if re.search('Yield outside function', output):
            names = re.findall(r'%s( Yield outside function)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you used the function keyword \"yield\".\n"%n[0] +
                                  "However, this was not inside of a function.\n" +
                                  "Check your indentation if you thought it was.\n\n")

        #Return with argument used with yield (E0106)
        if re.search('Return with argument inside generator', output):
            names = re.findall(r'%s( Return with argument inside generator\n.*return )(.*)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you used \"return\" with the argument \"%s\".\n"%(n[0],n[4]) +
                                  "However, in the same generator you used a \"yield\" statement.\n" +
                                  "You cannot mix these two statements unless your \"return\" statement has no argument.\n" +
                                  "If you wanted to return None with your return statement, simply use \"return\"\n")

        #Method is hidden by instance attr from ancestor class (E0202)
        if re.search ('An attribute inherited from .* hide.*', output):
            names = re.findall(r'%s( An attribute inherited from )(.*)( hide.*)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you defined a method which is hidden by an instance attribute of the ancestor class %s.\n"%(n[0],n[4]) +
                                  "If you do not want this attribute, consider re-structuring your inheritance.\n\n")

        #Instance member called before assignment (E0203)
        if re.search('Acces to member .* before its definition line .*', output):
            names = re.findall(r'%s( Access to member )(.*)( before its definition line )(.*)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you tried to access the instance object %s.\n"%(n[0],n[4]) +
                                  "However, you have not defined that object until line %s.\n"%n[6] +
                                  "You should move the definition of the object to a line before the one where you access it.\n\n")

        #Non-static method lacks "self" as first parameter (E0211)
        if re.search('Method has no argument', output):
            names = re.findall(r'%s( Method has no argument)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you define a method with no argument.\n"%n[0] +
                                  "Non-static methods need \"self\" as the first argument.\n" +
                                  "If you meant to make a static method, you need \"@staticmethod\" on the line prior to the method definition.\n\n")

        #Method has something other than "self" as first argument (E0213)
        if re.search(r'Method should have \"self\" as first argument', output):
            names = re.findall(r'%s( Method should have \"self\" as first argument)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you define a method with arguments.\n"%n[0] +
                                  "In any method with arguments, the first argument must be \"self\".")

        #Class tries to implement non-class interface (E0221)
        if re.search('Interface resolved to .* is not a class', output):
            names = re.findall(r'%s( Interface resolved to )(.*)( is not a class)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you tried to implement the interface %s.\n"%(n[0],n[4]) +
                                  "However, this interface is not defined as a class.\n" +
                                  "Classes can only implement class interfaces.\n\n")

        #Method in interface missing in class (E0222)
        if re.search('Missing method .* from .* interface', output):
            names = re.findall(r'%s( Missing method )(.*)( from )(.*)(interface)'%DIG, output)

            for n in names:
                pretty_output += ("Interface %s has method %s.\n"%(n[6],n[4]) +
                                  "However, the class on line %s which implements this interface does not define this method.\n\n"%n[0])

        #Non ASCII characters found w/o encoding (E0501)
        if re.search('Non ascii characters', output):
            names = re.findall(r'%s( Non ascii characters)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you have non ASCII characters.\n"%n[0] +
                                  "However, you have not included any encoding, so python cannot handle these characters.\n\n")

        #Recognized encoding but it seems wrong (E0502)
        if re.search('Wrong encoding specified', output):
            names = re.findall(r'%s( Wrong encoding specified [(])(.*)([)])'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you have specified the encoding %s.\n"%(n[0],n[4]) +
                                  "However, this encoding really doesn't seem right.\n" +
                                  "If the encoding isn't right, Python will interpret your code poorly.\n\n")

        #Unrecognized encoding (E0503)
        if re.search('Unkown encoding specified', output):
            names = re.findall(r'%s( Unknown encoding specified [(])(.*)([)])'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you have specified the encoding %s.\n"%(n[0],n[4]) +
                                  "However, python cannot recognize the encoding.\n\n")

        #Local var not yet defined (E0601)
        if re.search('Using variable .* before assignment', output):
            names = re.findall(r'%s( Using variable )(.*)( before assignment)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you referred to variable %s.\n"%(n[0],n[4]) +
                                  "However, this variable is assigned a value after you referred to it.\n" +
                                  "You should move the assignment to before the reference.\n\n")
        
        #Local var never defined (E0602)
        if re.search('Undefined variable', output):
            names = re.findall(r'%s( Undefined variable )(.*)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you referred to variable %s.\n"%(n[0],n[4]) +
                                  "However, you never define this variable.\n" +
                                  "If you want an objects without content, try assigning the variable to a basic class instance.\n\n")

        #Import something from a module that doesn't exist (E0611)
        if re.search('No name .* in module', output):
            names = re.findall(r'%s( No name )(.*)( in module )(.*)'%DIG, output)
            
            for n in names:
                pretty_output += ("On line %s you tried to import %s from module %s.\n"%(n[0],n[4],n[6]) +
                                  "However, %s does not exist in that module.\n"%n[4] +
                                  "Remember to use \"from <module.submodule> import <class>\" when importing a single class.\n\n")

        #Except clauses not in most-specific to least-specific order (E0701)
        if re.search('Bad except clauses order', output):
            names = re.findall(r'%s( Bad except clauses order)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you ordered your \"exempt\" clauses i.n a poorly.\n"%n[0] +
                                  "You should always order from most specific to least specific arguments.\n" +
                                  "Also, if you have an \"exempt\" clause without an argument, you should put that as your last clause.\n\n")

        #TypeError - class, instance string (E0702)
        if re.search('while only classes, instances, or string are allowed', output):
            names = re.findall(r'%s( Raising )(.*)( while only classes,)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you had a %s object.\n"%(n[0],n[4]) +
                                  "However, you could only use a class, instance, or string in this place.\n\n")

        #Wrong class given as arg to super class (E1003)
        if re.search('Bad first argument', output):
            names = re.findall(r'%s( Bad first argument )(.*)( given)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you used \"super\" with an incorrect argument.\n"%n[0] +
                                  "You have to use the current class as the first argument with \"super\"\n\n")

        #Tried to access non-existent member of variable (E1101, includes E1103)
        if re.search('.* has no .* member', output):
            names = re.findall(r'([:] )%s(.*)(Module .*)( has no )(.*)( member)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you tried to use the %s member of %s.\n"%(n[1],n[7],n[5]) +
                                  "However, %s does not exist for this object.\n\n"%n[7])

        #Called object which cannot be called (E1102)
        if re.search('is not callable', output):
            names = re.findall(r'(\d*)(,0[:] |[:] )(.*)( is not callable)', output)

            for n in names:
                pretty_output += ("On line %s you tried to call %s.\n"%(n[0],n[3]) +
                                  "However, %s is not a method, class, or function.\n" +
                                  "This means that the object is not callable.\n\n")

        #Assigning from function call that doesn't return anything (E1111)
        if re.search('Assigning to function call', output):
            names = re.findall(r'%s( Assigning to function call'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you assign a valuable to the return value of a function.\n"%n[0]+
                                  "However, this function does not return anything.\n" +
                                  "You can add a return statement to the function or simply call the function without capturing the value.\n\n")

        #Inefective statement (W0104)
        if re.search('Statement seems to have no efect', output):
            names = re.findall(r'%s( Statement seems to have)'%DIG, output)

            for n in names:
                pretty_output += ("The statement on line %s seems to have no effect.\n\n"%n[0])

        #Inefective STRING statement (W0105)
        if re.search('String statement has', output):
            names = re.findall(r'%s( String statement)'%DIG, output)

            for n in names:
                pretty_output += ("The string on line %s has no effect.\n"%n[0] +
                                  "Comments should have a hashtag (#) at the start of the line.\n" +
                                  "To display a string, you need to put \"print\" first.\n\n")

        #Semi-colon (W0301)
        if re.search('semicolon', output):
            names = re.findall(r'%s(.*semicolon.*)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you have an unnecessary semicolon.\n"%n[0] +
                                  "You don't need to put a semicolon at the end of a line in python.\n\n")

        #Bad amount of indentation (W0311)
        if re.search('Bad indentation', output):
            names = re.findall(r'%s( Bad indentation. Found )(.*)(, expected )(.*)'%DIG, output)

            for n in names:
                pretty_output += ("On line %s you have an unexpected amount of indentation.\n"%n[0] +
                                  "Instead of %s spaces, you had %s.\n\n"%(len(n[6]),len(4)))

        #Mixed tabs & spaces (W0312)
        if re.search('Found indentation with', output):
            names = re.findall(r'%s( Found indentation with '%DIG, output)

            for n in names:
                pretty_output += ("On line %s, you mixed tabs and spaces.\n"%n[0] +
                                  "Instead of tabs, use 4 spaces.\n\n")

        #Recognize "perfect" code
        if pretty_output == "--Code Analysis--\n\n\n":
            pretty_output += ("Congratulations, you have no errors in your code.\n" +
                              "Is it doing what you expected?\n\n")

        return pretty_output