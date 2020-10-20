#!/bin/python3

""" dx_job_monitor
Finds failed jobs in 002 projects and sends messages to alert the team
"""

import sys

import dxpy

sys.path.append("../hermes")

import hermes


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


def get_failed_jobs_per_project(projects):
    """ Return dict of project2jobs

    Args:
        projects (list): List of project ids

    Returns:
        dict: Dict of project to failed jobs
    """

    project2jobs = {}

    for project in projects:
        project_id = project.describe()["id"]
        project_name = project.describe()["name"]
        jobs = dxpy.find_jobs(
            project=project_id, state="failed",
            created_after=f"-24h"
        )
        project2jobs.setdefault(project_name, [])

        for job in jobs:
            job = dxpy.DXJob(job["id"])
            job_name = job.describe()["name"]
            project2jobs[project_name].append(job_name)

    return project2jobs


def send_msg_using_hermes(project2jobs):
    """ Sends msg using Hermes

    Args:
        project2jobs (dict): Dict of project to failed jobs
    """

    for project, jobs in project2jobs.items():
        if jobs == []:
            message = f"No jobs have failed in {project} the last 24h"
        else:
            jobs = ", ".join(jobs)
            message = f"The following jobs failed in {project} - {jobs}"

        hermes.main({"cmd": "msg", "message": message})


def main():
    projects = get_002_projects()
    project2jobs = get_failed_jobs_per_project(projects)
    send_msg_using_hermes(project2jobs)


if __name__ == "__main__":
    main()
