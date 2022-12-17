class PostwrittenScripter:
    CTRLS = ["THROTTLE", "YAW", "PITCH", "ROLL"]

    def __init__(self) -> None:
        self.script = []
        self.gradient = {c: 0 for c in self.CTRLS}
        self.control_values = {c: 0 for c in self.CTRLS}
        self.mag_dir = {c: 0 for c in self.CTRLS}

    def reset_mag_dir(self):
        self.mag_dir = {c: 0 for c in self.CTRLS}

    def update_mag_dir(self):
        for c in self.CTRLS:
            self.mag_dir[c] += self.gradient[c]

    def calc_gradient(self, new_control_values):
        grad = {c: new_control_values[c] - self.control_values[c] for c in self.CTRLS}

        return grad

    def is_zero_gradient(self):
        return sum(list(self.gradient.values())) == 0

    def check_event(self, new_control_values):
        grad = self.calc_gradient(new_control_values)

        if self.gradient == grad or self.is_zero_gradient():
            self.update_mag_dir()

        else:
            self.add_script_line()
            self.reset_mag_dir()

        self.gradient = grad
        self.control_values = new_control_values
        print(f"Grad: {self.gradient}")

    def add_script_line(self):
        line = ""
        mag_vals = set(self.mag_dir.values())
        mag = None

        for k in self.mag_dir:
            if self.mag_dir[k] > 0:
                line += k + "_INCR "
                mag = max(mag_vals)

            elif self.mag_dir[k] < 0:
                line += k + "_DECR "
                mag = abs(min(mag_vals))

        if mag:
            line += str(mag)
        
        if line:
            self.script.append(line)