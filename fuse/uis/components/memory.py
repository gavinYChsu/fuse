from typing import Optional

import gradio

import fuse.choices
from fuse import state_manager, translator
from fuse.common_helper import calculate_int_step
from fuse.types import VideoMemoryStrategy

VIDEO_MEMORY_STRATEGY_DROPDOWN : Optional[gradio.Dropdown] = None
SYSTEM_MEMORY_LIMIT_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global VIDEO_MEMORY_STRATEGY_DROPDOWN
	global SYSTEM_MEMORY_LIMIT_SLIDER

	VIDEO_MEMORY_STRATEGY_DROPDOWN = gradio.Dropdown(
		label = translator.get('uis.video_memory_strategy_dropdown'),
		choices = fuse.choices.video_memory_strategies,
		value = state_manager.get_item('video_memory_strategy')
	)
	SYSTEM_MEMORY_LIMIT_SLIDER = gradio.Slider(
		label = translator.get('uis.system_memory_limit_slider'),
		step = calculate_int_step(fuse.choices.system_memory_limit_range),
		minimum = fuse.choices.system_memory_limit_range[0],
		maximum = fuse.choices.system_memory_limit_range[-1],
		value = state_manager.get_item('system_memory_limit')
	)


def listen() -> None:
	VIDEO_MEMORY_STRATEGY_DROPDOWN.change(update_video_memory_strategy, inputs = VIDEO_MEMORY_STRATEGY_DROPDOWN)
	SYSTEM_MEMORY_LIMIT_SLIDER.release(update_system_memory_limit, inputs = SYSTEM_MEMORY_LIMIT_SLIDER)


def update_video_memory_strategy(video_memory_strategy : VideoMemoryStrategy) -> None:
	state_manager.set_item('video_memory_strategy', video_memory_strategy)


def update_system_memory_limit(system_memory_limit : float) -> None:
	state_manager.set_item('system_memory_limit', int(system_memory_limit))
