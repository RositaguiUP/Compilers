
# return error message

# simple string errors:
def stringError(gramToComp, line):
    #error = f"Missing '{gramToComp}' in line {line}"
    error = [f"Missing '{gramToComp}'", line]
    return error

# token errors:
def tokenError(token, line):
    #error = f"Missing '{token}' in line {line}"
    error = [f"Missing '{token}'", line]
    return error