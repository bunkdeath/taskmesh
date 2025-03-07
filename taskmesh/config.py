class Config:
    def __init__(self):
        self.TASK_ENABLED = True

    def background_task_status(self, status: bool):
        self.TASK_ENABLED = status
