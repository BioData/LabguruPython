from pojo import Response


class Experiment(Response):
    def __init__(self, token=None, project_id=None, milestone_id=None, id=None, title=None, owner=None,
                 project_owner=None, **kwargs):
        Response.__init__(self, token, **kwargs)
        self.project_id = project_id
        self.milestone_id = milestone_id
        self.id = id
        self.title = title
        self.owner = owner
        self.project_owner = project_owner
