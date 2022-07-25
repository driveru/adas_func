from diffgram import Project

def setup_project(project_name, client_id, client_secret, host = 'http://localhost:8085'):
    project = Project(
        project_string_id = project_name,
        host = host,
        client_id = client_id,
        client_secret = client_secret
    )

    if not project:
        raise Exception('Cannot setup project')

    return project
