import opentrons.execute
import requests
import json
import import_ipynb
import csv
from labguru import Labguru


experiment_id = 512
lab = Labguru(login='login@gmail.com', password='123password')

# get Labguru elements
experiment = lab.get_experiment(experiment_id)
plate_element = lab.get_elements_by_type(experiment_id, 'plate')[0].get_data()
sample_element = lab.get_elements_by_type(experiment_id, 'samples')[0]
forms_elements = lab.get_elements_by_type(experiment_id, 'form')
steps_element = lab.get_elements_by_type(experiment_id, 'steps')[0]
attachments_element = lab.get_elements_by_type(experiment_id, 'attachments')[0]

# get data from elements
samples = sample_element.get_data()
data = forms_elements[1].get_data()

# opentrons protocol
protocol = opentrons.execute.get_protocol_api('2.8')
protocol.home()

plate1 = protocol.load_labware(data['source_plate'], 4)
plate2 = protocol.load_labware(data['destination_plate'], 7)
tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 10)
p50_multi = protocol.load_instrument('p50_multi', 'right', tip_racks=[tiprack_1])

# iterating samples and stocks from Labguru
for sample_index, sample in enumerate(samples):
    p50_multi.pick_up_tip()
    p50_multi.aspirate(data['transfer_volume'], plate1.rows()[0][sample_index])
    for stock_index, stock in enumerate(sample['stocks']):
        p50_multi.dispense(10, plate2.rows()[0][stock_index])

    # update stocks volume in Labguru
    sample_element.update_stock_amount(sample['id'], stock['id'], data['transfer_volume'], 'volume', data['unit'])
    # add step to Labguru with some tracking information
    steps_element.add_step(f'transfer {data["transfer_volume"]} {data["unit"]}, of {stock["name"]} id {stock["id"]}')

    p50_multi.drop_tip()


# create csv file from Labguru plate
file_name = 'Cell culture - Assay Preparation.csv'
with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'coordinates', 'samples', 'stock', 'concentration'])
    for cell in plate_element:
        writer.writerow([cell['id'], cell['coordinates'], cell['samples'][0],
                         cell['samples_metadata'][str(cell['samples'][0])]['stocks'],
                         cell['samples_metadata'][str(cell['samples'][0])]['concentration']])

with open(file_name, 'rb') as file:
    attachment = file.read()

# upload file to Labguru
attachment_reponse = requests.post(f'{lab.session.url}/api/v1/attachments',
        data={
            'item[title]': file_name,
            'item[attachable_type]': 'Knowledgebase::AbstractDocument',
            'item[attach_to_uuid]': experiment.uuid,
            'token': lab.session.token,
        },
        files={'item[attachment]': (file_name, attachment)},
    )

# add attachment to attachments_element
attachments_element.add_attachment(attachment_reponse.json()['id'])

protocol.home()
