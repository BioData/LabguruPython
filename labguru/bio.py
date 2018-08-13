from .project import Project


class Genes(Project):
    def __init__(self, token=None, id=None, title=None, marker=None, description=None, sequence=None, **kwargs):
        Project.__init__(self, token=token, id=id, title=title, description=description, **kwargs)
        self.marker = marker
        self.sequence = sequence
        self.endpoint = '/api/v1/genes.json'
        self.specific_endpoint = '/api/v1/genes/{id}.json'


class Primers(Project):
    def __init__(self, token=None, id=None, title=None, description=None, sequence=None, **kwargs):
        Project.__init__(self, token=token, id=id, title=title, description=description, **kwargs)
        self.sequence = sequence
        self.endpoint = '/api/v1/primers.json'
        self.specific_endpoint = '/api/v1/primers/{id}.json'


class Plasmids(Project):
    def __init__(self, token=None, id=None, title=None, description=None, sequence=None, **kwargs):
        Project.__init__(self, token=token, id=id, title=title, description=description, **kwargs)
        self.sequence = sequence
        self.endpoint = '/api/v1/plasmids.json'
        self.specific_endpoint = '/api/v1/plasmids/{id}.json'


class Proteins(Project):
    def __init__(self, token=None, id=None, name=None, alternative_name=None, description=None, **kwargs):
        Project.__init__(self, token=token, id=id, description=description, **kwargs)
        self.name = name
        self.alternative_name = alternative_name
        self.endpoint = '/api/v1/proteins.json'
        self.specific_endpoint = '/api/v1/proteins/{id}.json'


class Sequences(Project):
    def __init__(self, token=None, id=None, title=None, description=None, seq=None, **kwargs):
        Project.__init__(self, token=token, id=id, title=title, description=description, **kwargs)
        self.seq = seq
        self.endpoint = '/api/v1/sequences.json'
        self.specific_endpoint = '/api/v1/sequences/{id}.json'


class Lipids(Project):
    def __init__(self, token=None, id=None, member_id=None, name=None, description=None, **kwargs):
        Project.__init__(self, token=token, id=id, description=description, **kwargs)
        self.member_id = member_id
        self.name = name
        self.endpoint = '/api/v1/lipids.json'
        self.specific_endpoint = '/api/v1/lipids/{id}.json'


class Antibodies(Project):
    def __init__(self, token=None, id=None, title=None, description=None, **kwargs):
        Project.__init__(self, token=token, id=id, title=title, description=description, **kwargs)
        self.endpoint = '/api/v1/antibodies.json'
        self.specific_endpoint = '/api/v1/antibodies/{id}.json'


class Bacteria(Project):
    def __init__(self, token=None, id=None, name=None, description=None, **kwargs):
        Project.__init__(self, token=token, id=id, description=description, **kwargs)
        self.name = name
        self.endpoint = '/api/v1/bacteria.json'
        self.specific_endpoint = '/api/v1/bacteria/{id}.json'
