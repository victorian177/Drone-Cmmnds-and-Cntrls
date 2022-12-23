from utils import create_folder, list_files, printer, string_stripper, write_file


class PrewrittenScripter:
    SCRIPTING_ROOT_PATH = "scriptings/prewritten"
    LEFT_JS = "THROTTLE", "YAW"
    RIGHT_JS = "PITCH", "ROLL"
    ACTIONS = {
        0: "THROTTLE_INCR",
        1: "THROTTLE_DECR",
        2: "YAW_DECR",
        3: "YAW_INCR",
        4: "PITCH_INCR",
        5: "PITCH_DECR",
        6: "ROLL_DECR",
        7: "ROLL_INCR",
    }
    STRIP_LIST = "_INCR", "_DECR"

    def __init__(self) -> None:
        self.check_default_path()
        self.script = []

    def get_script(self):
        return self.script

    def write_file(self, filename):
        with open(self.SCRIPTING_ROOT_PATH + "/" + filename + ".txt", "w") as f:
            f.writelines(self.script)

    def list_scripts(self):
        return list_files(self.SCRIPTING_ROOT_PATH)

    def check_default_path(self):
        create_folder(self.SCRIPTING_ROOT_PATH)

    def script_formatter(self, actions, intensity):
        action_nums = tuple(int(i) for i in actions.split())
        intensity_num = int(intensity)

        action_list = [self.ACTIONS[a] for a in action_nums]
        len_action_list = len(action_list)

        script_line = []

        if len_action_list == 1:
            script_line.append(action_list[0])
        elif len_action_list == 2:
            validity = self.action_validator(action_list)
            if validity:
                for i in range(len_action_list):
                    script_line.append(action_list[i])

        script_line.append(intensity_num)

        if len_action_list > 2:
            raise Exception("Invalid number of inputs.")

        script_line = [str(s) for s in script_line]
        script_line = " ".join(script_line)
        script_line += "\n"

        return script_line

    def action_validator(self, action_list):
        action_list_stripped = [
            string_stripper(a, self.STRIP_LIST) for a in action_list
        ]
        action_js = ["l" if a in self.LEFT_JS else "r" for a in action_list_stripped]
        return action_js[0] != action_js[1]

    def prewritten_script_input(self):
        num_of_actions = len(self.ACTIONS)
        actions = {k: self.ACTIONS[k] for k in range(num_of_actions)}
        printer(f"Actions: {actions}")

        while True:
            actions = input("Enter number(s) (associated with action, 'q' to quit): ")
            if actions == "q":
                break

            intensity = input("Enter intensity: ")
            script_line = self.script_formatter(actions, intensity)
            if script_line:
                self.script.append(script_line)

    def prewritten_script_writer(self):
        self.script = []
        self.prewritten_script_input()

        if self.script:
            printer(f"Scripts: {self.list_scripts()}")
            filename = input("Enter filename: ")

            write_file(
                folder_path=self.SCRIPTING_ROOT_PATH,
                file_contents=self.script,
                filename=filename,
            )


if __name__ == "__main__":
    prewrttn_scrptr = PrewrittenScripter()
    prewrttn_scrptr.prewritten_script_writer()