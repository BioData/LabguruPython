from labguru import Labguru, Session, UnAuthorizeException, NotFoundException, Project


def get_token():
    lab = Labguru(login='xtutran@gmail.com', password='Password123')
    return lab


def create_project(lab, title, description=None):
    if lab:
        return lab.create_new_project(title, description)


def get_project(lab, project_id):
    if lab:
        project = lab.get_project(project_id)
        return project


def get_all_projects(lab, page):
    if lab:
        return lab.get_all_projects(page)


def main():
    lab = get_token()
    print(lab.session.token)

    print(create_project(lab, 'Create_Project_From_Python_Package', 'Testing'))

    projects = get_all_projects(lab, 1)
    for proj in projects:
        print(proj)

if __name__ == '__main__':
    main()
