import supervisely as sly
import globals as g
# import datasets
# import classes
# import settings
# import metrics


def init(data, state):
    # state['collapsed1'] = False
    # state['disabled1'] = False
    state['done1'] = False

    state["GTteamId"] = g.team_id
    state["GTworkspaceId"] = g.workspace_id
    state["PRteamId"] = g.team_id
    state["PRworkspaceId"] = g.workspace_id

    #@TODO: uncomment for prod
    #state["gtProjectId"] = None
    #state["predProjectId"] = None

    # @TODO: comment for prod
    state["gtProjectId"] = 3642
    state["predProjectId"] = 3641


def restart(data, state):
    state['done1'] = False


@g.my_app.callback("set_projects")
@sly.timeit
def set_projects(api: sly.Api, task_id, context, state, app_logger):

    g.gt_project_info = api.project.get_info_by_id(state['gtProjectId'], raise_error=True)
    g.pr_project_info = api.project.get_info_by_id(state['predProjectId'], raise_error=True)

    fields = []
    for i in range(1, 6):
        value = True if i != 2 else False  # 2: input -> datasets
        done = True if i < 2 else False
        fields.append({"field": f"state.collapsed{i}", "payload": value})
        fields.append({"field": f"state.disabled{i}", "payload": value})
        fields.append({"field": f"state.done{i}", "payload": done})

    extra_fields = [
        {"field": "state.activeStep", "payload": 2},
        {"field": "state.gtProjectId", "payload": g.gt_project_info.id},
        {"field": "state.gtProjectName", "payload": g.gt_project_info.name},
        {"field": "state.gtProjectPreviewUrl",
         "payload": g.api.image.preview_url(g.gt_project_info.reference_image_url, 100, 100)},

        {"field": "state.predProjectId", "payload": g.pr_project_info.id},
        {"field": "state.predProjectName", "payload": g.pr_project_info.name},
        {"field": "state.predProjectPreviewUrl",
         "payload": g.api.image.preview_url(g.pr_project_info.reference_image_url, 100, 100)},
    ]
    fields.extend(extra_fields)
    api.app.set_fields(task_id, fields)
