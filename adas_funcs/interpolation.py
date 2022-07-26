import json

def interpolate(annotation_path, file_id):

    with open(annotation_path, 'r') as f:
        annotation = json.loads(f.read())

    packet_map = { }

    for sequence in annotation[str(file_id)]['sequence_list']:
        if len(sequence['instance_list']) == 0:
            continue

        frame_num = 0
        points = []
        seq_num = sequence['number']

        sequence['instance_list'].sort(key = lambda x: x['frame_number'])

        inst = sequence['instance_list'][0]
        if inst['frame_number'] != 0:
            raise Exception('First frame is not annotated')

        packet_map[0] = [{
            'type' : inst['type'],
            'label_file_id' : inst['label_file_id'],
            'frame_number' : 0,
            'number' : inst['frame_number'],
            'points' : inst['points']
        }]

        for inst in sequence['instance_list']:
            for i in range(frame_num + 1, inst['frame_number']):
                if not points:
                    continue

                if i in packet_map.keys():
                    raise Exception(f'There are more than one instance on the frame {i}')
                else:
                    packet_map[i] = [{
                        'type' : type,
                        'label_file_id' : label_file_id,
                        'frame_number' : i,
                        'number' : seq_num,
                        'points' : points
                    }]

            type = inst['type']
            label_file_id = inst['label_file_id']
            frame_num = inst['frame_number']
            points = inst['points']

    return packet_map
