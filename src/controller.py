
class PIDController:
    """PID controller for smoothing autonomous driving commands."""

    def __init__(self, kp, ki, kd, output_limits=(-1.0, 1.0)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_min, self.output_max = output_limits

        self.integral = 0.0
        self.previous_error = 0.0
        self.initialized = False

    def reset(self):
        """Reset controller history."""
        self.integral = 0.0
        self.previous_error = 0.0
        self.initialized = False

    def update(self, error, dt):
        """Calculate a bounded PID correction."""
        if dt <= 0:
            raise ValueError("dt must be greater than zero")

        self.integral += error * dt
        derivative = 0.0

        if self.initialized:
            derivative = (error - self.previous_error) / dt

        output = (
            self.kp * error
            + self.ki * self.integral
            + self.kd * derivative
        )

        self.previous_error = error
        self.initialized = True

        return max(self.output_min, min(self.output_max, output))
