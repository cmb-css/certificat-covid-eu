import json


if __name__ == '__main__':
    with open('certificat-covid-eu.json', 'rt') as f_in, open('certificat-covid-eu-clean.json', 'wt') as f_out:
        for line in f_in:
            data = json.loads(line)
            user = data['user']
            if '(' in user:
                pos = user.find('(')
                user = u'hidden {}'.format(user[pos:])
                data['user'] = user
            f_out.write('{}\n'.format(data))
