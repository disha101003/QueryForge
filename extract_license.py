import json

with open('queryforge.json') as fp:
    data = json.load(fp)

licenses = set()


for component in data['components']:
    for license_info in component.get('licenses', []):
        license = license_info.get('license', {})
        if 'id' in license:
            licenses.add(license['id'])

print(licenses)
