from labguru import Labguru, Session, UnAuthorizeException, Project
from labguru.exception import NotFoundException


def get_token():
    lab = Labguru(login='xtutran@gmail.com', password='Password123')
    return lab


def main():
    lab = get_token()
    print(lab.session.token)

    projects = lab.list_projects(page_num=1)
    for proj in projects:
        # print(proj)
        if proj.id == 141:
            print(proj)
            #print(proj.create_new_folder('New Folder 2'))
            print('current folders')
            for f in proj.get_current_folders():
                print(f)
            print('future folders')
            for f in proj.get_future_folders():
                print(f)
            print('pass folders')
            for f in proj.get_past_folders():
                print(f)

    # print(lab.get_folder(folder_id='41'))
    #
    # for folder in lab.list_folders(page_num=1):
    #     print(folder)

if __name__ == '__main__':
    main()
