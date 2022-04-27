import sys
import requests
import getopt
from requests.auth import HTTPBasicAuth


def get_feed_id(project_id, feed, access_token):
    url = 'https://feeds.dev.azure.com/devops2192/' + project_id + \
        '/_apis/packaging/feeds/' + feed + '?api-version=6.0-preview.1'
    header = {'Content-Type': 'application/json'}
    body = ''
    result = requests.get(url=url, auth=HTTPBasicAuth(
        '', access_token), headers=header)
    if result.status_code != 200:
        print('Cannot get feed id for: ' + feed +
               ' Error: ' + str(result.status_code))
        return result.status_code
    retu = result.json()
    return retu["id"]



def get_view_id(project_id, feed_id, view, access_token):
    url = 'https://feeds.dev.azure.com/devops2192/' + project_id + \
        '/_apis/packaging/feeds/' + feed_id + '/views/' + \
        view + '?api-version=6.0-preview.1'
    header = {'Content-Type': 'application/json'}
    body = ''
    result = requests.get(url=url, auth=HTTPBasicAuth(
        '', access_token), headers=header)
    if result.status_code != 200:
        print('Cannot get feed id for: ' + feed_id +
               ' Error: ' + str(result.status_code))
        return result.status_code
    retu = result.json()
    return retu["id"]


def change_artifact_view(project_id, feed_id, access_token, artifact_name, artifact_group, artifact_version, view_id):
    url = 'https://pkgs.dev.azure.com/devops2192/'+ project_id + \
        '/_apis/packaging/feeds/'+ feed_id + \
        '/maven/packagesBatch?api-version=5.0-preview.1'
    header = {'Content-Type': 'application/json'}
    body = {"data": {"viewId": view_id}, "operation": 0,
            "packages": [{"group": artifact_group, "artifact": artifact_name, "version": artifact_version}]}
    result = requests.post(url=url, json=body, auth=HTTPBasicAuth(
        '', access_token), headers=header)
    if result.status_code != 202:
        print('Cannot add artifact: ' + artifact_name + ' to view: ' +
             view_id +  ' Error: ' + str(result.status_code))
        return result.status_code
    print('Your request sent to processing. Status: ', result)
    return result



def main(arguments):
    """
    adds artifact in feed to specific view
    :param arguments: sys.argv
    """
    project_id = ''
    feed = ''
    access_token = ''
    artifact_name = ''
    artifact_group = ''
    artifact_version= ''
    view = ''

    # read argument from command line
    try:
        opts, args = getopt.getopt(arguments, "hp:f:t:a:g:v:w:",
                                   ["project_id=", "feed=", "PAT=", "artifact=", "group=", "version=", "view="])
    except getopt.GetoptError:
        print('change_view.py -p <project_id> -f <feed> -t <PAT>  -a <artifact_name> -g <artifact_group> -v <artifact '
              'ver> -w <view>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(  
                'change_view.py -p <project_id> -f <feed> -t <PAT>  -a <artifact_name> -g <artifact_group> -v <artifact '
                'ver> -w <view>')
            sys.exit()
        elif opt in ("-p", "--project_id"):
            project_id = arg
        elif opt in ("-f", "--feed"):
            feed = arg
        elif opt in ("-t", "--PAT"):
            access_token = arg
        elif opt in ("-a", "--artifact"):
            artifact_name = arg
        elif opt in ("-g", "--group"):
            artifact_group = arg
        elif opt in ("-v", "--version"):
            artifact_version = arg
        elif opt in ("-w", "--view"):
            view = arg

    
    # get required IDS from API
    feed_id = get_feed_id(project_id, feed, access_token)
    view_id = get_view_id(project_id, feed, view, access_token)

    # print operation details
    print('Project ID: ', project_id)
    print('Feed: ', feed)
    print('Feed ID: ', feed_id)
    print('View: ', view)
    print('view ID: ', view_id)
    print('Artifact: ', artifact_name)
    print('Version: ', artifact_version)
    print('Artifact_group', artifact_group)

    
    # changinf view for  artifact
    change_artifact_view(project_id, feed_id, access_token,
                         artifact_name, artifact_version, artifact_group, view_id)
                         
if __name__ == "__main__":
    main(sys.argv[1:])