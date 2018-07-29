from project import Project


class Experiment(Project):
    def __init__(self, token=None, project_id=None, milestone_id=None, id=None, title=None, **kwargs):
        Project.__init__(self, token, id, title, **kwargs)
        self.project_id = project_id
        self.milestone_id = milestone_id
        self.endpoint = '/api/v1/experiments.json'
        self.specific_endpoint = '/api/v1/experiments/{id}.json'


