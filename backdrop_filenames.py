import csv, json, re, random


with open('m_v1_moview_with_backdrop_all.csv', 'w') as wf:
    with open('m_v1_movies_with_backdrop.csv', 'r') as f:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(wf, fieldnames=reader.fieldnames + ['local_backdrop_links'])
        writer.writeheader()
        for row in reader:
            if row['backdrops']:
                if ',' in row['backdrops']:
                    images = row['backdrops'].split(',')
                    row['backdrops'] = json.dumps(images)
                    local_names = []
                    for image in images:
                        name = re.sub('/', '~', '_'.join(row['movie_title'].split()))+ '_' + str(random.randrange(100000, 1000000)) + '.jpg'
                        local_names.append(name)
                    row['local_backdrop_links'] = json.dumps(local_names)
                else:
                    image = row['backdrops']
                    row['backdrops'] = json.dumps([image])
                    name = re.sub('/', '~', '_'.join(row['movie_title'].split()))+ '_' + str(random.randrange(100000, 1000000)) + '.jpg'
                    row['local_backdrop_links'] = json.dumps([name])

            if row['posters']:
                posters = row['posters'].split(',')
                row['posters'] = json.dumps(posters)
            else:
                row['posters'] = json.dumps([row['posters']])
            
            writer.writerow(row)