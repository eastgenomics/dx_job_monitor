#!/bin/python3

""" dx_job_monitor
Finds failed jobs in 002 projects and sends messages to alert the team
"""

from collections import defaultdict
import sys

import dxpy

sys.path.append("../hermes/")

import hermes

TOKEN_FILE_PATH = "../hermes/slack_token.txt"


def get_002_projects():
    """ Return list of 002 projects

    Returns:
        list: List of project ids
    """

    project_objects = []
    projects = dxpy.find_projects(name="002_*", name_mode="glob")

    for project in projects:
        project_objects.append(dxpy.DXProject(project["id"]))

    return project_objects


def get_jobs_per_project(projects):
    """ Return dict of project2state2jobs

    Args:
        projects (list): List of project ids

    Returns:
        dict: Dict of project to state to jobs
    """

    project2jobs = defaultdict(lambda: defaultdict(list))
    project_no_run = []

    for project in projects:
        project_id = project.describe()["id"]
        project_name = project.describe()["name"]
        jobs = dxpy.find_jobs(project=project_id, created_after=f"-24h")

        jobs = [job for job in jobs]

        if jobs:
            for job in jobs:
                job = dxpy.DXJob(job["id"])
                job_name = job.describe()["name"]
                job_state = job.describe()["state"]
                project2jobs[project_name][job_state].append(job_name)
        else:
            project_no_run.append(project_name)

    return project2jobs, project_no_run


def send_msg_using_hermes(project2jobs, project_no_run):
    """ Sends msg using Hermes

    Args:
        project2jobs (dict): Dict of project to failed jobs
    """

    project_no_pb = []

    for project in project2jobs:
        states = project2jobs[project]

        if "failed" in states:
            for state in states:
                jobs = ", ".join(project2jobs[project][state])

                if state == "failed":
                    message = (
                        f":x:: The following jobs failed in {project} - {jobs}"
                    )
                    hermes.main(
                        {
                            "token_file": TOKEN_FILE_PATH,
                            "channel": "egg-alerts",
                            "cmd": "msg", "message": message
                        }
                    )
        else:
            project_no_pb.append(project)

    # No pb projects
    if project_no_pb:
        job_run_but_no_pb_projects = ", ".join(project_no_pb)
        message = (
            ":heavy_check_mark:: Jobs have been run in the last 24h and"
            f" none have failed for: {job_run_but_no_pb_projects}"
        )
        hermes.main(
            {
                "token_file": TOKEN_FILE_PATH, "channel": "egg-logs",
                "cmd": "msg", "message": message
            }
        )

    # Nothing run in the last 24h
    if project_no_run:
        nb_projects_no_jobs = len(project_no_run)
        message = (
            ":heavy_check_mark:: No jobs have been ran in the last 24h"
            f" for {nb_projects_no_jobs} projects"
        )
        hermes.main(
            {
                "token_file": TOKEN_FILE_PATH, "channel": "egg-logs",
                "cmd": "msg", "message": message
            }
        )


def main():
    projects = get_002_projects()
    project2jobs, project_no_run = get_jobs_per_project(projects)
    send_msg_using_hermes(project2jobs, project_no_run)


if __name__ == "__main__":
    main()
