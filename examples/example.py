from labguru import Labguru, Session, UnAuthorizeException, Project
from labguru.exception import NotFoundException


def get_token():
    lab = Labguru(login='xtutran@gmail.com', password='Password123')
    return lab


def main():
    lab = get_token()
    print(lab.session.token)

    # print(lab.add_project(title='new add project'))
    # lab.update_project(project_id='20333', title='Update title for 201', description='Update description for 201')

    # for proj in lab.list_projects(page_num=1):
    #     print(proj)

    proj141 = lab.get_project(project_id='141')
    # for folder in proj141.list_folders():
    #     print(folder)

    folder251 = lab.get_folder(folder_id='251')
    b = folder251.add_experiment(title="exp 2")

    print(b)


    # projects = lab.list_projects(page_num=1)
    # for proj in projects:
    #     # print(proj)
    #     if proj.id == 141:
    #         print(proj)
    #         #print(proj.add_folder('New Folder 2'))
    #         print('current folders')
    #         for f in proj.get_current_folders():
    #             print(f)
    #         print('future folders')
    #         for f in proj.get_future_folders():
    #             print(f)
    #         print('pass folders')
    #         for f in proj.get_past_folders():
    #             print(f)

    # print(lab.get_folder(folder_id='41'))
    #
    # for folder in lab.list_folders(page_num=1):
    #     print(folder)

if __name__ == '__main__':
    main()
