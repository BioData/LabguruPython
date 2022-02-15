import json

from labguru import Labguru


def get_token():
    lab = Labguru(login='login@gmail.com', password='123password')
    return lab


def main():
    lab = get_token()
    print(lab.session.token)

    # project
    # print(prj)
    # print(lab.update_project(project_id=prj.id, title='Update title for 201', description='Update description for 201'))

    # for proj in lab.list_projects(page_num=1):
    #     print(proj)

    # proj141 = lab.get_project(project_id='11')
    # print(proj141.id)

    # folder
    # for folder in lab.list_folders(page_num=1):
    #     print(folder)

    # print(lab.add_folder(project_id='141', title='new add folder', description='new des'))
    # for folder in lab.list_folders(project_id='141', page_num=1):
    #     print(folder)

    # experiment
    # for exp in lab.list_experiments(page_num=1):
    #     print(exp.id)

    # print(lab.get_experiment(experiment_id='827'))

    # section
    # print(lab.add_experiment_procedure(container_id=827, name='test1'))
    # print(lab.find_experiment_procedures(name='test1')[0].id)
    # print(lab.get_experiment_procedure(section_id=5515).container_id)
    # print(lab.update_experiment_procedure(section_id=5515, name='new name'))
    # print(lab.list_experiment_procedures(experiment_id=827, page_num=1)[-1].id)

    # print(lab.add_element(section_id=5567, data='<p>hello world</p>'))


    # for section in lab.list_experiment_procedures(experiment_id='1'):
    #     print(section)



    # element
    # print(lab.get_element(element_id='1601').container_id)
    # print(lab.get_experiment_procedure(1154).container_id)
    # print(lab.update_element(element_id=8117, name='test1', data='<p> add text </p>'))
    # print(lab.get_elements_by_type(experiment_id=586, element_type='plate')[0])
    # print(lab.get_elements_by_type(experiment_id=586, element_type='form')[1].description)
    # print(lab.get_elements_by_type(experiment_id=804, element_type='plate')[0].name)
    # print(json.loads(lab.get_elements_by_type(experiment_id=804, element_type='plate')[1].data)['wells'])
    # print(json.loads(lab.get_elements_by_type(experiment_id=804, element_type='samples')[0].data).get('samples'))
    #
    # print(lab.get_elements_by_type(experiment_id=804, element_type='plate')[1].get_data())
    # print(lab.get_elements_by_type(experiment_id=804, element_type='samples')[0].get_data())
    # print(lab.get_elements_by_type(experiment_id=806, element_type='form')[1])
    # print(lab.add_element(section_id=5478, data=None, element_type='steps'))
    # print(lab.get_element(8034))

    #inventory item
    # print(lab.add_inventory_item(name='test_lib', item_type='cell_lines'))
    # print(lab.get_inventory_item(item_id=329, item_type='cell_lines'))
    # print(lab.update_inventory_item(item_id=329, item_type='cell_lines', name='new name'))
    # print(lab.list_inventory_items(item_type='cell_lines', page_num=1)[1].name)
    # print(lab.list_inventory_generic_items(item_type='services', page_num=1)[1].name)

    # print(lab.add_stock(stock_name='test1', storage_id=2, storage_type="System::Storage::Box",
    #                     stockable_type="Biocollections::CellLine", stockable_id=329))
    # print(lab.find_stocks(stock_name='test_2')[0].id)
    # print(lab.update_stock(stock_id=966, volume=5))

    # sample_element = lab.get_elements_by_type(experiment_id=811, element_type='samples')[0]
    # sample_element_data = sample_element.get_data()
    # sample_id = sample_element_data[0].get('id')
    # stock_id = sample_element_data[0].get('stocks')[0]['id']
    # print(sample_element.update_stock_amount(sample_id, stock_id, amount_used='1', unit_type='volume', unit_type_name='mL'))

    # steps_element = lab.get_elements_by_type(experiment_id=812, element_type='steps')[0]
    # print(steps_element.add_step('ho'))

    # attachment_element = lab.add_element(section_id=5511, data='', element_type='attachments')
    # print(attachment_element.add_attachment(attachment_id=3159))

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
    #
    # print(lab.get_folder(folder_id='41'))
    #
    # for folder in lab.list_folders(page_num=1):
    #     print(folder)

if __name__ == '__main__':
    main()
