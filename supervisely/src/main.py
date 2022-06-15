import supervisely as sly
import globals as g
from ui.ui import init


def main():
    sly.logger.info("Script arguments", extra={
        "context.teamId": g.team_id,
        "context.workspaceId": g.workspace_id
    })

    data = {}
    state = {}

    from ui.test.test import init_demo_sample
    init_demo_sample(data, state)

    # init data for UI widgets
    init(data, state)
    g.my_app.compile_template(g.root_source_dir)
    g.my_app.run(data=data, state=state)


# @TODO: GTteamId - gtProjectId - camel case
if __name__ == "__main__":
    sly.main_wrapper("main", main)
