class Config:
    def __init__(self):
        self.TASK_ENABLED = True
        self.ack_message_on_error = True

    def background_task_status(self, status: bool):
        self.TASK_ENABLED = status

    def ack_on_error(self, status: bool):
        self.ack_message_on_error = status
