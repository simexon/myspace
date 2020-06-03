from flask import escape
def validate(string):
    return escape(string.strip())

print (validate("    Hello    <b>"))