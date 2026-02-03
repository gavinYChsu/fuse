from typing import List, Optional

import gradio

import fuse.choices
from fuse import state_manager, translator
from fuse.common_helper import get_first
from fuse.jobs import job_manager
from fuse.types import JobStatus
from fuse.uis.core import register_ui_component

JOB_LIST_JOB_STATUS_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None


def render() -> None:
	global JOB_LIST_JOB_STATUS_CHECKBOX_GROUP

	if job_manager.init_jobs(state_manager.get_item('jobs_path')):
		job_status = get_first(fuse.choices.job_statuses)

		JOB_LIST_JOB_STATUS_CHECKBOX_GROUP = gradio.CheckboxGroup(
			label = translator.get('uis.job_list_status_checkbox_group'),
			choices = fuse.choices.job_statuses,
			value = job_status
		)
		register_ui_component('job_list_job_status_checkbox_group', JOB_LIST_JOB_STATUS_CHECKBOX_GROUP)


def listen() -> None:
	JOB_LIST_JOB_STATUS_CHECKBOX_GROUP.change(update_job_status_checkbox_group, inputs = JOB_LIST_JOB_STATUS_CHECKBOX_GROUP, outputs = JOB_LIST_JOB_STATUS_CHECKBOX_GROUP)


def update_job_status_checkbox_group(job_statuses : List[JobStatus]) -> gradio.CheckboxGroup:
	job_statuses = job_statuses or fuse.choices.job_statuses
	return gradio.CheckboxGroup(value = job_statuses)
