from project import Project


class Experiment(Project):
    def __init__(self, token=None, project_id=None, milestone_id=None, id=None, title=None, **kwargs):
        Project.__init__(self, token, id, title, **kwargs)
        self.project_id = project_id
        self.milestone_id = milestone_id
        self.endpoint = '/api/v1/experiments.json'
        self.specific_endpoint = '/api/v1/experiments/{id}.json'


class Section(Project):
    def __init__(self, token=None, container_id=None, id=None, name=None, section_type=None, container_type=None, **kwargs):
        Project.__init__(self, token, id, **kwargs)
        self.container_id = container_id
        self.name = name
        self.section_type = section_type
        self.container_type = container_type
        self.endpoint = '/api/v1/element_containers.json'
        self.specific_endpoint = '/api/v1/element_containers/{id}.json'



