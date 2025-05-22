from typing import Tuple
import os

# поиск файлов в папке
def create_xml_filename_list(dir_path: str, file_ext: str, postfix_str: str) -> Tuple[Tuple[str, str, str], ...]:
    return tuple((root, os.path.splitext(name)[0], os.path.splitext(name)[1])
                 for root, dirs, files in os.walk(top=dir_path, topdown=True)
                 for name in files
                 if name.endswith(file_ext) and (not name.endswith(postfix_str+file_ext) and not name.endswith('_test'+file_ext)))

# замена в файле по маске и другие изменения
def update_xml_scheme(xml_filename: Tuple[str, str, str], replace_samples_list: Tuple[Tuple[str, str], ...]) -> str:
    xml_data = ''
    with open(f'{xml_filename[0]}/{xml_filename[1]}{xml_filename[2]}', mode='r', encoding='utf-8') as xml_file:
        xml_data = xml_file.read()

    for replace_sample in replace_samples_list:
        xml_data = xml_data.replace(replace_sample[0], replace_sample[1])

    start_index = 600
    for i in range(xml_data.count('<pac:fact>')):
        uuid_start_pos = xml_data.find('<!-- <af:ID>', start_index) + len('<!-- <af:ID>')
        fact_uuid = xml_data[uuid_start_pos: uuid_start_pos+36]
        start_index = uuid_start_pos + 37
        uuid_insert_pos = xml_data.find('</af:assignmentInfo>', start_index) + len('</af:assignmentInfo>')
        xml_data = f'{xml_data[:uuid_insert_pos]}\n{' ' * 8}<pac:uuid>{fact_uuid}</pac:uuid>{xml_data[uuid_insert_pos:]}'

    return xml_data

# сохраняем новую версию xml с постфиксом в имени
def save_new_xml(xml_data: str, xml_filename: Tuple[str, str, str], postfix_str: str = '_new') -> None:
    with open(f'{xml_filename[0]}/{xml_filename[1]}{postfix_str}{xml_filename[2]}', mode='w', encoding='utf-8') as xml_file:
        xml_file.write(xml_data)

def main():
    replace_samples_list = (('<data xmlns="urn://egisso-ru/msg/10.06.S/1.0.2" xmlns:pac="urn://egisso-ru/types/package-RAF/1.0.3" '
                             'xmlns:smev="urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1" '
                             'xmlns:egisso="urn://egisso-ru/types/basic/1.0.4" xmlns:prsn="urn://egisso-ru/types/prsn-info/1.0.3" '
                             'xmlns:af="urn://egisso-ru/types/assignment-fact/1.0.3">',
                             '<data xmlns="urn://egisso-ru/msg/10.06.S/1.1.0" xmlns:pac="urn://egisso-ru/types/package-RAF/1.1.0" '
                             'xmlns:smev="urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1" '
                             'xmlns:egisso="urn://egisso-ru/types/basic/1.0.8" xmlns:prsn="urn://egisso-ru/types/prsn-info/1.0.4" '
                             'xmlns:af="urn://egisso-ru/types/assignment-fact/1.0.8" xmlns:prsn2="urn://egisso-ru/types/prsn-basis/1.0.2">'),
                            ('pac:packageID', 'pac:packageId'),
                            ('af:OSZCode', 'af:oszCode'),
                            ('af:MSZ_receiver', 'af:mszReceiver'),
                            ('af:reason_persons', 'af:reasonPersons'),
                            ('<prsn:prsnInfo>', '<prsn2:basisPerson><prsn:prsnInfo>'),
                            ('</prsn:prsnInfo>', '</prsn:prsnInfo></prsn2:basisPerson>'),
                            ('af:LMSZID', 'af:lmszId'),
                            ('af:categoryID', 'af:categoryId'),
                            ('af:decision_date', 'af:decisionDate'),
                            ('af:assignment_info', 'af:assignmentInfo'),
                            ('af:monetary_form', 'af:monetaryForm'),
                            ('af:natural_form', 'af:naturalForm'),

                            ('<af:ID>', '<!-- <af:ID>'), ('</af:ID>', '</af:ID> -->'),
                            ('<af:OKEICode>', '<!-- <af:OKEICode>'), ('</af:OKEICode>', '</af:OKEICode> -->'),
                            ('<af:criteria>', '<!-- <af:criteria>'), ('</af:criteria>', '</af:criteria> -->'),
                            ('<pac:lastChanging>', '<!-- <pac:lastChanging>'), ('</pac:lastChanging>', '</pac:lastChanging> -->'))

    xml_filename_list = create_xml_filename_list(dir_path='input', postfix_str='_10.06.S-1.1.0', file_ext='.xml')
    for xml_filename in xml_filename_list:
        xml_data = update_xml_scheme(xml_filename, replace_samples_list)
        save_new_xml(xml_data, xml_filename, postfix_str='_10.06.S-1.1.0')

if __name__ == '__main__':
    main()