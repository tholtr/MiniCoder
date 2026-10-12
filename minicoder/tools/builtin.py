"""内置工具集合。"""

from __future__ import annotations

from pathlib import Path

from minicoder.tools.apply_patch import create_apply_patch_tool
from minicoder.tools.ask_user import create_ask_user_tool
from minicoder.tools.edit import create_edit_tool
from minicoder.tools.delete import create_delete_tool
from minicoder.tools.diagnostics import create_diagnostics_tool
from minicoder.tools.git_diff import create_git_diff_tool
from minicoder.tools.git_log import create_git_log_tool
from minicoder.tools.git_status import create_git_status_tool
from minicoder.tools.fetch import create_fetch_tool
from minicoder.tools.glob import create_glob_tool
from minicoder.tools.grep import create_grep_tool
from minicoder.tools.ls import create_ls_tool
from minicoder.tools.python_exec import create_python_exec_tool
from minicoder.tools.processes import create_process_tools
from minicoder.tools.read_multi import create_read_multi_tool
from minicoder.tools.registry import ToolRegistry
from minicoder.tools.think import create_think_tool
from minicoder.tools.shell import create_shell_tool
from minicoder.tools.tree import create_tree_tool
from minicoder.tools.view import create_view_tool
from minicoder.tools.web_search import create_web_search_tool
from minicoder.tools.write import create_write_tool
from minicoder.tools.descriptions import apply_agent_tool_description
from minicoder.utils.sandbox_access import SandboxAccess
from minicoder.agent.processes import ProcessManager


def create_builtin_registry(
    root: str | Path,
    include_mutation_tools: bool = False,
    include_execution_tools: bool = False,
    include_network_tools: bool = False,
    access: SandboxAccess | None = None,
    include_ask_user: bool = True,
    include_think: bool = True,
    include_web_search: bool = True,
    process_manager: ProcessManager | None = None,
) -> ToolRegistry:
    """创建第一阶段默认可用工具。

    默认只注册只读工具。写入类工具必须显式启用，方便后续接确认机制。
    """

    tools = [
        create_ls_tool(root, access=access),
        create_view_tool(root, access=access),
        create_grep_tool(root, access=access),
        create_glob_tool(root, access=access),
        create_tree_tool(root, access=access),
        create_git_status_tool(root, access=access),
        create_git_diff_tool(root, access=access),
        create_git_log_tool(root, access=access),
        create_diagnostics_tool(root, access=access),
        create_read_multi_tool(root, access=access),
    ]
    if include_think:
        tools.insert(9, create_think_tool())
    if include_ask_user:
        tools.append(create_ask_user_tool())
    if include_mutation_tools:
        tools.extend(
            [
                create_write_tool(root, access=access),
                create_edit_tool(root, access=access),
                create_delete_tool(root, access=access),
                create_apply_patch_tool(root, access=access),
            ]
        )
    if include_execution_tools:
        tools.extend(
            [
                create_shell_tool(root, access=access),
                create_python_exec_tool(root, access=access),
            ]
        )
        if process_manager is not None:
            tools.extend(create_process_tools(root, process_manager, access=access))
    if include_network_tools:
        tools.append(create_fetch_tool())
        if include_web_search:
            tools.append(create_web_search_tool())
    return ToolRegistry([apply_agent_tool_description(tool) for tool in tools])
