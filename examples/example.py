from labguru import Labguru, Folder, Project


def get_token():
    lab = Labguru(login='xtutran@gmail.com', password='Password123')
    return lab


def main():
    lab = get_token()
    print(lab.session.token)

    # prj = lab.add_project(title='new _add project')
    # print(prj)
    # print(lab.update_project(project_id=prj.id, title='Update title for 201', description='Update description for 201'))
    #
    # for proj in lab.list_projects(page_num=1):
    #     print(proj)
    #
    # proj141 = lab.get_project(project_id='141')
    # print(proj141.id)

    # for folder in lab.list_folders(page_num=1):
    #     print(folder)

    # print(lab.add_folder(project_id='141', title='new add folder', description='new des'))
    # for folder in lab.list_folders(project_id='141', page_num=1):
    #     print(folder)

    for exp in lab.list_experiments(page_num=1):
        print(exp.id)

    # print(lab.get_experiment(experiment_id='141'))
    # lab.add_section(experiment_id='1', name='Tran add section')

    print(lab.get_experiment(experiment_id='1'))

    print(lab.get_section(section_id='1'))

    for section in lab.list_sections(experiment_id='1'):
        print(section)

    # print(lab.get_folder(folder_id='291'))

    # folder251 = lab.get_folder(folder_id='251')
    # b = folder251.add_experiment(title="exp 2")

    # print(b)


    # projects = lab.list_projects(page_num=1)
    # for proj in projects:
    #     # print(proj)
    #     if proj.id == 141:
    #         print(proj)
    #         #print(proj.register('New Folder 2'))
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
