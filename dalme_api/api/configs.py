import json
import os
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_api.access_policies import ConfigsAccessPolicy


class Configs(viewsets.ViewSet):
    """ API endpoint for retrieving configuration files """
    permission_classes = (ConfigsAccessPolicy,)

    def list(self, request):
        try:
            result = self.traverse_directory(os.path.join('dalme_app', 'config'))
            status = 201
        except Exception as e:
            result = {'error': 'The following error occured while trying to get the file: ' + str(e)}
            status = 400
        return Response(result, status)

    @action(detail=False, methods=['post'])
    def get(self, request):
        if request.data.get('target') is None:
            result = {'error': 'Target missing from request.'}
            status = 400

        else:
            result = []
            path = request.data['path'].split(',') if request.data.get('path') is not None else ''

            if request.data.get('base') is not None:
                files = [request.data['target'], 'base']
            elif type(request.data['target']) is list:
                files = request.data['target']
            else:
                files = [request.data['target']]

            if request.data.get('buttons') is not None:
                files = [i['button'] for i in files if request.user.has_perm(i.get('permissions', 'auth.view_user'))]

            try:
                for file in files:
                    with open(os.path.join('dalme_app', 'config', *path, '_' + file + '.json'), 'r') as fp:
                        result.append(json.load(fp))

                status = 201

            except FileNotFoundError:
                try:
                    for file in files:
                        with open(os.path.join('dalme_app', 'config', *path, file + '.json'), 'r') as fp:
                            result.append(json.load(fp))

                    status = 201

                except Exception as e:
                    result = {'error': 'The following error occured while trying to get the file: ' + str(e)}
                    status = 400

            except Exception as e:
                result = {'error': 'The following error occured while trying to get the file: ' + str(e)}
                status = 400

        return Response(result, status)

    @action(detail=False, methods=['post'])
    def save(self, request):
        target = request.data.get('target')
        path = request.data.get('path')
        payload = request.data.get('payload')

        if target is None or payload is None:
            return Response({'error': 'Target and Text must be supplied.'}, 400)

        else:
            path = path.split(',') if path is not None else ''
            file = os.path.join('dalme_app', 'config', *path, '_' + target + '.json')

            if not os.path.exists(file):
                file = os.path.join('dalme_app', 'config', *path, target + '.json')

                if not os.path.exists(file):
                    return Response({'error': 'Filepath could not be found.'}, 400)

            try:
                with open(file, 'w') as fp:
                    fp.write(json.dumps(payload, indent=2))

                return Response('ok', 201)

            except Exception as e:
                return Response({'error': 'The following error occured while trying to get the file: ' + str(e)}, 400)

    def traverse_directory(self, path):
        tree = []
        for item in os.scandir(path):
            if item.is_file():
                if not item.name.startswith('.'):
                    file_name = item.name[1:-5] if item.name[0] == '_' else item.name[0:-5]
                    tree.append({'text': file_name, 'icon': 'fas fa-file-code', 'class': 'b'})
            if item.is_dir():
                tree.append({'text': item.name, 'icon': 'fas fa-folder', 'class': 'a', 'nodes': self.traverse_directory(item.path)})

        return sorted(sorted(tree, key=lambda e: e['text']), key=lambda e: e['class'])
