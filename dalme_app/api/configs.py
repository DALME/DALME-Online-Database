import json
import os
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_app.access_policies import ConfigsAccessPolicy


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
            except Exception as e:
                result = {'error': 'The following error occured while trying to get the file: ' + str(e)}
                status = 400
        return Response(result, status)

    def traverse_directory(self, path):
        tree = []
        for item in os.scandir(path):
            if item.is_file():
                file_name = item.name[1:-5] if item.name[0] == '_' else item.name[0:-5]
                tree.append({'text': file_name, 'icon': 'fas fa-file-code', 'class': 'b'})
            if item.is_dir():
                tree.append({'text': item.name, 'icon': 'fas fa-folder', 'class': 'a', 'nodes': self.traverse_directory(item.path)})
        return sorted(sorted(tree, key=lambda e: e['text']), key=lambda e: e['class'])
