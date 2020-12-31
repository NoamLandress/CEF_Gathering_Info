class system_info:
    def __init__(self, command, command_output, error="No error received"):
        self.command = command
        self.command_output = command_output
        self.error = error

    def __repr__(self):
        delimiter = "\n-----------------------------------\n"
        return str(delimiter + "command: " + self.command + '\n' + "output: " + self.command_output + '\n' + "error: " + self.error)


noam = system_info("x", "y")
print(repr(noam))